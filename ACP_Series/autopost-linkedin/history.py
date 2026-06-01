import sys
from database import SessionLocal, Post

# Reconfigure terminal encoding to UTF-8 on Windows to handle emojis correctly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

db = SessionLocal()

posts = (
    db.query(Post)
    .order_by(Post.id.desc())
    .all()
)

for post in posts:

    print(
        post.id,
        post.topic,
        post.style,
        post.created_at
    )