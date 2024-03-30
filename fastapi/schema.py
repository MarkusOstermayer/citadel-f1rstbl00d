# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FirstBloodCreate(BaseModel):
    date: Optional[datetime] = None
    user_id: int
    event_id: int
    challenge_id: int