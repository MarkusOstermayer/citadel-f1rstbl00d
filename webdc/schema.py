# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FirstBloodCreate(BaseModel):
    date: Optional[datetime] = None
    username: str
    event_id: int
    challenge_id: int
    challenge_name: str
    challenge_category: str
    challenge_difficulty: str
