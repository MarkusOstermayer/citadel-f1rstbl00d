# schemas.py
from pydantic import BaseModel, validator
from typing import Optional, Union
from datetime import datetime


class FirstBloodCreate(BaseModel):
    """
    Schema for creating a new FirstBlood entry

    The "date" field can be either a datetime object or a unix timestamp
    """

    date: Optional[Union[datetime, int]] = None
    username: str
    event_id: str
    challenge_id: str
    challenge_name: str
    challenge_category: str
    challenge_difficulty: str

    # Convert unix timestamp to datetime object if needed
    @validator("date", pre=True)
    def unix_timestamp_to_datetime(cls, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
