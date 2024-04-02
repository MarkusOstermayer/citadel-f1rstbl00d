# schemas.py
from pydantic import BaseModel, validator
from typing import Optional, Union
from datetime import datetime


class FirstBloodCreate(BaseModel):
    date: Optional[Union[datetime, int]] = None
    username: str
    event_id: int
    challenge_id: int
    challenge_name: str
    challenge_category: str
    challenge_difficulty: str

    @validator('date', pre=True)
    def unix_timestamp_to_datetime(cls, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%S')