from poster import post_to_linkedin
from generator import generate_post
from database import SessionLocal, Post
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def run():

    topic, style, post = generate_post()

    success = post_to_linkedin(post)

    db = SessionLocal()

    record = Post(
        topic=topic,
        style=style,
        post_text=post,
        status="posted" if success else "failed"
    )

    db.add(record)
    db.commit()

    print("\nTOPIC\n")
    print(topic)

    print("\nSTYLE\n")
    print(style)

    print("\nSTATUS\n")
    print("posted" if success else "failed")

    print("\nPOST\n")
    print(post)


if __name__ == "__main__":
    run()