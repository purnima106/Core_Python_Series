from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///posts.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    topic = Column(String)
    style = Column(String)

    post_text = Column(Text)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    linkedin_post_id = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)


Base.metadata.create_all(engine)

