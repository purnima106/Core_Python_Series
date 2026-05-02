# ============================================================
# analyze_pr — Groq/OpenAI-style function-calling agentic loop
# ============================================================
# Flow:
#   1. Send PR URL + available tools to Groq LLM
#   2. If LLM returns tool_calls → execute them → feed results back
#   3. Loop until LLM produces a structured JSON answer
#   4. Parse JSON safely, fallback to raw text if parsing fails
# ============================================================

import os
import re
import json
from app.mcp.tools.github import mcp, get_pr_diff  # MCP instance + tool function
from groq import AsyncGroq

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# ── System prompt: enforce structured JSON output ────────────
SYSTEM_PROMPT = """You are a senior code reviewer. You analyze GitHub Pull Request diffs
and return your review as **strictly valid JSON** — no markdown, no explanation, no text
outside the JSON object.

Required JSON schema:
{
  "summary": "<one-paragraph summary of changes>",
  "risk": "<low | medium | high>",
  "issues": ["<issue 1>", "<issue 2>"],
  "suggestions": ["<suggestion 1>", "<suggestion 2>"]
}

Rules:
- "risk" must be exactly one of: low, medium, high
- "issues" and "suggestions" are arrays of strings (can be empty [])
- Do NOT wrap the JSON in markdown code fences
- Do NOT include any text before or after the JSON object
- Return ONLY the JSON object
"""

# ── Registry of callable tool functions ──────────────────────
# Maps tool name → actual Python async function
# Add more tools here as you build them
TOOL_REGISTRY = {
    "get_pr_diff": get_pr_diff,
}


async def analyze_pr(pr_url: str) -> dict:
    """
    Analyze a GitHub PR using Groq LLM with function calling.

    Returns:
        dict with "review" key containing the AI's final review text.
    """

    # ── Step 0: Convert MCP tools → Groq/OpenAI function format ──
    mcp_tools = await mcp.list_tools()
    groq_tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            },
        }
        for t in mcp_tools
    ]

    # ── Step 1: Build messages with system + user prompt ─────────
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"Fetch and review this GitHub PR: {pr_url}\n\n"
                "Use the get_pr_diff tool to fetch the diff, then analyze it.\n"
                "Return your review as a single JSON object with keys: "
                "summary, risk, issues, suggestions.\n"
                "Return ONLY valid JSON. No other text."
            ),
        }
    ]

    # ── Step 2–5: Agentic loop ───────────────────────────────────
    # Keep calling the model until it stops requesting tools
    max_iterations = 10  # safety net to prevent infinite loops

    for _ in range(max_iterations):
        # Call Groq with tools
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            tools=groq_tools,
            tool_choice="auto",   # let the model decide
            messages=messages,
        )

        choice = response.choices[0]
        message = choice.message

        # ── Check: Does the response contain tool_calls? ─────────
        if not message.tool_calls:
            # No tool calls → LLM is done, parse structured JSON
            return parse_review_json(message.content)

        # ── tool_calls exist → execute each one ──────────────────
        # First, append the assistant's message (with tool_calls) to history
        messages.append({
            "role": "assistant",
            "content": message.content,          # may be None
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in message.tool_calls
            ],
        })

        # Process each tool call
        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f"🔧 Tool called: {fn_name}({fn_args})")

            # Look up the function in our registry
            fn = TOOL_REGISTRY.get(fn_name)
            if fn is None:
                tool_output = f"Error: Unknown tool '{fn_name}'"
            else:
                try:
                    # Execute the actual Python function
                    tool_output = await fn(**fn_args)
                except Exception as e:
                    tool_output = f"Error executing {fn_name}: {str(e)}"

            print(f"✅ Tool result length: {len(str(tool_output))} chars")

            # Append tool result as a "tool" message
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_output),
            })

        # Loop continues → model will now see the tool results
        # and either call more tools or produce the final answer

    # If we exhausted max_iterations, return fallback
    return {
        "summary": "Error: Too many tool call iterations.",
        "risk": "high",
        "issues": ["Review could not be completed — exceeded max iterations"],
        "suggestions": ["Please try again with a different PR URL"],
    }


# ── JSON parser with fallback ────────────────────────────────
def parse_review_json(raw_text: str) -> dict:
    """
    Safely parse the LLM's response into structured JSON.
    Falls back to raw text wrapped in the expected schema if parsing fails.
    """
    if not raw_text:
        return {
            "summary": "No response received from AI.",
            "risk": "high",
            "issues": ["Empty response"],
            "suggestions": ["Try again"],
        }

    # Try direct JSON parse first
    try:
        data = json.loads(raw_text)
        return normalize_review(data)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from markdown code fences (```json ... ```)
    match = re.search(r"```(?:json)?\s*\n?(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            return normalize_review(data)
        except json.JSONDecodeError:
            pass

    # Try finding any JSON object in the text
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            return normalize_review(data)
        except json.JSONDecodeError:
            pass

    # All parsing failed → wrap raw text as fallback
    print(f"⚠️ Could not parse JSON, returning raw text")
    return {
        "summary": raw_text,
        "risk": "unknown",
        "issues": [],
        "suggestions": [],
    }


def normalize_review(data: dict) -> dict:
    """Ensure all expected keys exist with correct types."""
    return {
        "summary": str(data.get("summary", "")),
        "risk": str(data.get("risk", "unknown")).lower(),
        "issues": [str(i) for i in data.get("issues", [])],
        "suggestions": [str(s) for s in data.get("suggestions", [])],
    }


# ── How the agentic loop works ───────────────────────────────
#
#  Iteration 1:
#    User   → "Fetch and review this PR: ..."
#    System → "You are a senior code reviewer. Return ONLY JSON."
#    Groq   → tool_calls: [get_pr_diff(pr_url=...)]
#    Us     → execute get_pr_diff → get the diff text
#    Us     → append tool result to messages
#
#  Iteration 2:
#    Groq   → sees diff → returns structured JSON review
#    Us     → parse JSON safely → return clean dict to API
#
# ─────────────────────────────────────────────────────────────