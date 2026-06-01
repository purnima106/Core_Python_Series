import os
import random
from groq import Groq

from dotenv import load_dotenv
from topics import TOPICS

load_dotenv()

# Initialize the Groq client
# It automatically picks up the GROQ_API_KEY environment variable
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_post():

    topic = random.choice(TOPICS)

    prompt = f"""
    You are a senior DevOps engineer with 5 to 8 years of experience.

    Write an engaging, professional LinkedIn post about:
    {topic}

    Audience:
    Intermediate to Advanced DevOps and SRE Professionals.

    Requirements:
    - Include a strong and attention-grabbing hook.
    - Use structural formatting (clear paragraphs and bullet points).
    - Keep it educational and highly valuable.
    - Add a brief call to action or thought-provoking question at the end.
    - Include 3-4 relevant hashtags.
    Length:
    180-220 words

    Format:
    1. Hook
    2. Insight
    3. Practical takeaway
    4. CTA

    Do not sound AI-generated.
    Do not use generic motivational statements.
    Provide one actionable learning.
    - Add emojis to the post to make it more engaging.

    Tone:
    Professional, authoritative, and engaging.

    """

    # We use llama-3.3-70b-versatile for rich, high-quality technical content.
    # You can also use "llama-3.1-8b-instant" for faster/lighter generation.
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return topic, response.choices[0].message.content