import os
import random
from groq import Groq

from dotenv import load_dotenv
from topics import TOPICS, STYLES
from database import SessionLocal, Post


load_dotenv()

# Initialize the Groq client
# It automatically picks up the GROQ_API_KEY environment variable
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_post():

    topic = get_next_topic()
    style = get_next_style()

    prompt = f"""
    You are a senior DevOps engineer with 5 to 8 years of experience.

    Write an engaging, professional LinkedIn post about:
    {topic}

    Writing Style / Angle:
    {style} (Write the post matching this specific style or narrative angle)

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

    return topic, style, response.choices[0].message.content

def get_next_topic():

    db = SessionLocal()

    recent_topics = (
        db.query(Post.topic)
        .order_by(Post.id.desc())
        .limit(10)
        .all()
    )

    recent_topics = [t[0] for t in recent_topics]

    available_topics = [
        topic
        for topic in TOPICS
        if topic not in recent_topics
    ]

    if not available_topics:
        available_topics = TOPICS

    return random.choice(available_topics)

def get_next_style():

    db = SessionLocal()

    recent_styles = (
        db.query(Post.style)
        .order_by(Post.id.desc())
        .limit(5)
        .all()
    )

    recent_styles = [s[0] for s in recent_styles]

    available_styles = [
        style
        for style in STYLES
        if style not in recent_styles
    ]

    if not available_styles:
        available_styles = STYLES

    return random.choice(available_styles)