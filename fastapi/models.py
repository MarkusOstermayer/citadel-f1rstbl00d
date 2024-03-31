# models.py
from sqlalchemy import Column, Integer, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FirstBlood(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    event_id = Column(Integer, nullable=False)
    challenge_id = Column(Integer, nullable=False)
    was_sent = Column(Boolean, default=False)
    __table_args__ = (
        UniqueConstraint("event_id", "challenge_id", name="_event_challenge_uc"),
    )
