import sys
from generator import generate_post

from database import SessionLocal
from database import Post

# Reconfigure terminal encoding to UTF-8 on Windows to handle emojis correctly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")



def run():

    topic, style, post = generate_post()

    db = SessionLocal()

    record = Post(
        topic=topic,
        style=style,
        post_text=post,
        status="generated"
    )

    db.add(record)
    db.commit()

    print("\nTOPIC\n")
    print(topic)

    print("\nPOST\n")
    print(post)


if __name__ == "__main__":
    run()