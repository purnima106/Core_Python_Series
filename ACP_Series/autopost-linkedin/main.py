from generator import generate_post

from database import SessionLocal
from database import Post


def run():

    topic, post = generate_post()

    db = SessionLocal()

    record = Post(
        topic=topic,
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