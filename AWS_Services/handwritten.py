import json
import boto3
import base64
import re
from io import BytesIO
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor
import csv
import io
from datetime import datetime

s3 = boto3.client("s3")
textract = boto3.client("textract")
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")


# -------------------------
# Extract AWB from Textract
# -------------------------
def extract_awb(lines):
    candidates = []

    for line in lines:
        numbers = re.findall(r"\b\d{10,16}\b", line)
        for num in numbers:
            # skip 12-digit numbers — those are E-Way Bills
            if len(num) == 12:
                continue
            candidates.append((num, line.lower()))

    for num, text in candidates:
        if "awb" in text or "barcode" in text:
            return num

    if candidates:
        return max(candidates, key=lambda x: len(x[0]))[0]

    return None


# -------------------------
# Rotate image if needed
# -------------------------
def rotate_if_needed(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    if image.height > image.width:
        image = image.rotate(90, expand=True)
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


# -------------------------
# Compress image aggressively for Bedrock (max size: 5MB per image)
# -------------------------
def compress_image(image_bytes, quality=60, max_dimension=1920):
    """
    Aggressively compress image to stay within Bedrock's 5MB limit per image.
    Reduces dimensions and quality to minimize file size.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    
    # Resize if too large
    if image.width > max_dimension or image.height > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    
    # If still too large, reduce quality further
    while buffer.tell() > 4500000 and quality > 30:  # Keep under 4.5MB to be safe
        buffer = BytesIO()
        quality -= 5
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
    
    return buffer.getvalue()


# -------------------------
# Preprocess for stamp detection
# -------------------------
def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = ImageEnhance.Contrast(image).enhance(2.5)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    image = ImageEnhance.Color(image).enhance(1.5)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()


# -------------------------
# Preprocess for Handwriting Detection (Higher Contrast)
# -------------------------
def preprocess_for_handwriting(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    # Increase contrast significantly for handwriting clarity
    image = ImageEnhance.Contrast(image).enhance(3.0)
    image = ImageEnhance.Sharpness(image).enhance(2.5)
    image = ImageEnhance.Brightness(image).enhance(1.1)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()


# -------------------------
# Extract JSON from Claude
# -------------------------
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return {
        "awb_number": None,
        "signature_present": False,
        "stamp_present": False,
        "handwritten_present": False,
        "handwritten_details": {}
    }


# -------------------------
# Detect and Extract Handwritten Text - IMPROVED
# -------------------------
def detect_handwritten_text(original_base64, textract_lines=None):

    textract_context = ""
    if textract_lines:
        textract_context = f"""
TEXTRACT RAW TEXT (character-level OCR of this document — use this to verify your readings):
{chr(10).join(textract_lines[:60])}

Use this as a spelling reference. If you read a word visually but it closely matches a word in the Textract output, prefer the Textract spelling.
"""

    prompt = f"""
You are reading a logistics POD (Proof of Delivery) document.

{textract_context}

YOUR ONLY JOB: Find handwritten operational remarks anywhere on this document.
Focus on what was received, how many, condition, by whom, and when.

---
STRICT RULES:
1. ONLY extract handwritten / pen / pencil written text
2. DO NOT extract printed template text
3. Write exactly what is written — do not autocorrect or guess
4. Use Textract reference to verify spellings of numbers and words
5. If nothing found for a field — return null
6. Return ONLY the JSON. No explanation.

---
LOOK FOR THESE ANYWHERE ON THE DOCUMENT:

- received_note: Any freehand confirmation of receipt written anywhere
- num_packages: Any handwritten number of boxes, cartons, pallets or pieces. If multiple types exist capture all rows exactly as written (e.g. "Small: 13, Big: 32, Total: 45")- weight_kg: Any handwritten weight value
- dimensions: Any handwritten dimension values
- damage_note: Any handwritten note about damage, shortage, missing items or condition
- delivery_receiver: Name of person who signed or received the shipment
- delivery_date: Any handwritten date of delivery or receipt
- pickup_date: Any handwritten date of pickup
- pickup_person: Name of pickup employee if written
- invoice_number: Any handwritten invoice or reference number
- eway_bill: Any handwritten eway bill reference or yes/no
- other_remarks: Any other handwritten note anywhere on the document that seems operationally relevant

---
RETURN ONLY THIS JSON:
{{
  "received_note": null,
  "num_packages": null,
  "weight_kg": null,
  "dimensions": null,
  "damage_note": null,
  "delivery_receiver": null,
  "delivery_date": null,
  "pickup_date": null,
  "pickup_person": null,
  "invoice_number": null,
  "eway_bill": null,
  "other_remarks": null,
  "signature_present": false,
  "stamp_present": false
}}
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": original_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:ap-south-1:752531001752:inference-profile/apac.anthropic.claude-sonnet-4-20250514-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )

        body = json.loads(response["body"].read())
        text_response = "".join(i["text"] for i in body["content"] if i["type"] == "text")
        
        # Extract JSON from response
        match = re.search(r"\{.*\}", text_response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception as e:
                print(f"JSON parsing error: {str(e)}")
                return {
                    "has_handwriting": False,
                    "handwritten_details": {},
                    "raw_response": text_response[:500]
                }
        
        return {
            "has_handwriting": False,
            "handwritten_details": {},
            "raw_response": text_response[:500]
        }
    except Exception as e:
        print(f"Error in handwritten text detection: {str(e)}")
        return {
            "has_handwriting": False,
            "handwritten_details": {},
            "error": str(e)
        }


# -------------------------
# Format handwritten details for CSV
# -------------------------
def format_handwriting_for_csv(handwriting_result):
    """
    Flatten the nested handwriting JSON into a single string for CSV storage.
    Makes it easy to read while preserving all extracted data.
    """
    if not handwriting_result.get("has_handwriting"):
        return "No handwriting detected"
    
    details = handwriting_result.get("handwritten_details", {})
    lines = []
    
    # From/To
    if details.get("from_to"):
        ft = details["from_to"]
        if ft.get("from") or ft.get("to"):
            lines.append(f"FROM: {ft.get('from', 'N/A')} | TO: {ft.get('to', 'N/A')}")
    
    # Consignor
    if details.get("consignor_details"):
        cd = details["consignor_details"]
        consignor_items = [v for v in [cd.get("sender_name"), cd.get("company_name"), cd.get("city"), cd.get("mobile")] if v]
        if consignor_items:
            lines.append(f"CONSIGNOR: {' | '.join(consignor_items)}")
    
    # Consignee
    if details.get("consignee_details"):
        ce = details["consignee_details"]
        consignee_items = [v for v in [ce.get("receiver_name"), ce.get("company_name"), ce.get("city"), ce.get("mobile")] if v]
        if consignee_items:
            lines.append(f"CONSIGNEE: {' | '.join(consignee_items)}")
    
    # Pickup
    if details.get("pickup_details"):
        pd = details["pickup_details"]
        pickup_items = [f"{k}={v}" for k, v in pd.items() if v and k != "signature"]
        if pickup_items:
            lines.append(f"PICKUP: {', '.join(pickup_items)}")
    
    # Shipment
    if details.get("shipment_details"):
        sd = details["shipment_details"]
        shipment_items = [f"{k}={v}" for k, v in sd.items() if v]
        if shipment_items:
            lines.append(f"SHIPMENT: {', '.join(shipment_items)}")
    
    # Delivery
    if details.get("delivery_section"):
        ds = details["delivery_section"]
        delivery_items = [v for v in [ds.get("receiver_name"), ds.get("delivery_date")] if v]
        if delivery_items or ds.get("signature_present"):
            sig_status = " [SIGNED]" if ds.get("signature_present") else ""
            lines.append(f"DELIVERY: {' | '.join(delivery_items)}{sig_status}")
    
    # Paperwork
    if details.get("paperwork_received"):
        pw = details["paperwork_received"]
        paperwork_items = [f"{k}={v}" for k, v in pw.items() if v]
        if paperwork_items:
            lines.append(f"PAPERWORK: {', '.join(paperwork_items)}")
    
    # Other notes
    if details.get("other_notes"):
        lines.append(f"NOTES: {details['other_notes']}")
    
    return " | ".join(lines) if lines else "No handwriting extracted"

def format_handwritten_notes(extracted):
    if not extracted:
        return "No handwritten notes"

    field_labels = [
        ("received_note", "Received"),
        ("num_packages", "Pkgs"),
        ("weight_kg", "Weight"),
        ("dimensions", "Dims"),
        ("damage_note", "Damage"),
        ("delivery_receiver", "Received By"),
        ("delivery_date", "Delivery Date"),
        ("pickup_date", "Pickup Date"),
        ("pickup_person", "Pickup By"),
        ("invoice_number", "Invoice"),
        ("eway_bill", "Eway"),
        ("other_remarks", "Remarks"),
    ]

    parts = [f"{label}: {extracted[key]}"
             for key, label in field_labels
             if extracted.get(key)]

    return " | ".join(parts) if parts else "No handwritten notes"


# Process Single Image
# -------------------------
def process_single(bucket, key):

    # --- Textract for AWB fallback ---
    textract_response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    lines = [b["Text"] for b in textract_response["Blocks"] if b["BlockType"] == "LINE"]
    textract_awb = extract_awb(lines)

    # --- Get image from S3 ---
    image_bytes = s3.get_object(Bucket=bucket, Key=key)["Body"].read()

    # --- Rotate if needed ---
    image_bytes = rotate_if_needed(image_bytes)

    # --- Compress original image to stay under 5MB ---
    image_bytes = compress_image(image_bytes, quality=70, max_dimension=2000)

    # --- Preprocess for enhanced analysis ---
    enhanced_image_bytes = preprocess_image(image_bytes)
    
    # --- Compress both to base64 ---
    hw_bytes = compress_image(image_bytes, quality=90, max_dimension=2000)
    original_base64 = base64.b64encode(image_bytes).decode("utf-8")
    hw_base64 = base64.b64encode(hw_bytes).decode("utf-8")
    enhanced_base64 = base64.b64encode(compress_image(enhanced_image_bytes, quality=70)).decode("utf-8")

    print(f"Original image size: {len(original_base64) / (1024*1024):.2f} MB base64")
    print(f"Enhanced image size: {len(enhanced_base64) / (1024*1024):.2f} MB base64")

    prompt = """
You are analyzing a POD (Proof of Delivery) document image.

Return exactly 4 fields: awb_number, signature_present, stamp_present, handwritten_present.

-------------------------------------

AWB NUMBER:

Look for a barcode on the document. Read the numeric digits printed directly below or above the barcode lines.

Rules:
- Length is typically 10 to 16 digits
- Appears near a scannable barcode (parallel vertical lines)
- Do NOT return: pin codes, phone numbers, invoice numbers, dates, employee IDs
- Return exactly as printed — no spaces, no dashes
- If no barcode or number found → return null

-------------------------------------

SIGNATURE:

A signature or sign of receipt can appear ANYWHERE on the document — not just in the SIGNATURE field.

Look across the ENTIRE document for:
- A cursive or stylized sign/scribble anywhere on the page
- A handwritten name anywhere (delivery section, margins, stamp area, paperwork section)
- Any pen mark that looks like someone acknowledging receipt
- Date written by hand anywhere on the page
- Initials or abbreviations signed by hand

Do NOT count:
- Pre-printed template text (part of original document design)
- Barcode numbers
- Printed field labels like "Name", "Signature", "Date"

Return true if ANY handwritten mark, name, or sign exists ANYWHERE on the document.
Return false ONLY if the entire document has zero handwritten content.

-------------------------------------

HANDWRITTEN:

Detect if ANY handwritten content exists ANYWHERE on the document.

This includes:
- Signatures
- Handwritten names
- Handwritten dates
- Scribbles, initials, pen marks
- Any human-written text or markings

Do NOT count:
- Printed text (template)
- Barcode numbers
- Machine-generated labels

Return:
- true → if ANY handwriting exists anywhere
- false → if NO handwriting at all

-------------------------------------

STAMP:

A stamp is ink applied to the document that has ALL of these properties:

1. NOT handwritten — no flowing strokes, no personal style, no pen marks
2. UNIFORM — all letters same size, same style, consistent ink
3. LARGER or MORE PROMINENT than the regular pre-printed template text
4. DIFFERENT ink color or ink density from the printed template

Scan the entire document and ask:
- Is there any block of text that stands out from the template?
- Does it look like it was applied ON TOP of the document?
- Is it bigger, bolder, or a different color?

Return true if found, else false.

-------------------------------------

Return ONLY this JSON:

{
  "awb_number": "string or null",
  "signature_present": true or false,
  "stamp_present": true or false,
  "handwritten_present": true or false
}
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": enhanced_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:ap-south-1:752531001752:inference-profile/apac.anthropic.claude-sonnet-4-20250514-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )

    body = json.loads(response["body"].read())
    text_response = "".join(i["text"] for i in body["content"] if i["type"] == "text")
    ai_result = extract_json(text_response)

    # --- IMPROVED: Detect and Extract Handwritten Text with structured data ---
    handwriting_result = detect_handwritten_text(hw_base64, lines)
    handwritten_notes = format_handwritten_notes(handwriting_result)

    if not handwritten_notes.strip():
        handwritten_notes = "No handwritten content"

    awb = textract_awb or ai_result.get("awb_number")
    pod_valid = bool(awb and ai_result["stamp_present"])

    return {
        "image": key,
        "awb_detected": awb,
        "signature_present": ai_result["signature_present"],
        "stamp_present": ai_result["stamp_present"],
        "handwritten_present": ai_result.get("handwritten_present", False),
        "handwritten_notes": handwritten_notes,
        "pod_valid": pod_valid
    }


# -------------------------
# Save CSV to S3
# -------------------------
def save_results_to_s3_csv(bucket, results):

    today = datetime.now().strftime("%Y-%m-%d")
    key = f"pod-val-results/{today}.csv"

    try:
        existing_obj = s3.get_object(Bucket=bucket, Key=key)
        existing_data = existing_obj["Body"].read().decode("utf-8")
        existing_content = "\n".join(existing_data.splitlines())
    except s3.exceptions.NoSuchKey:
        existing_content = ""

    string_buffer = io.StringIO()
    writer = csv.DictWriter(
        string_buffer,
        fieldnames=["image", "awb_detected", "signature_present", "stamp_present", "handwritten_present", "handwritten_notes", "pod_valid"]
    )

    if not existing_content:
        writer.writeheader()

    writer.writerows(results)
    new_content = string_buffer.getvalue()

    final_csv = existing_content.strip() + "\n" + new_content if existing_content else new_content

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=final_csv.encode("utf-8"),
        ContentType="text/csv"
    )

    return key


# -------------------------
# Lambda Handler
# -------------------------
def lambda_handler(event, context):

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    bucket = body["bucket"]
    keys = body.get("images") or [body["image"]]

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_single, bucket, key) for key in keys]
        for future in futures:
            results.append(future.result())

    output_key = save_results_to_s3_csv(bucket, results)

    formatted_results = "\n\n".join([
        f"Image: {r['image']}\n"
        f"AWB: {r['awb_detected']}\n"
        f"Signature: {r['signature_present']}\n"
        f"Stamp: {r['stamp_present']}\n"
        f"Handwritten: {r['handwritten_present']}\n"
        f"Handwritten Notes: {r['handwritten_notes']}\n"
        f"POD Valid: {r['pod_valid']}"
        for r in results
    ])
 
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "results": formatted_results,
            "csv_path": f"s3://{bucket}/{output_key}"
        })
    }