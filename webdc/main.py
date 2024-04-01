from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from db import get_db
from datetime import datetime, timezone
from typing import Optional
import models, schema
import os

# Start setup
load_dotenv()
app = FastAPI(title="FirstBlood API", description="API for FirstBlood records.")
security = HTTPBearer()


def authorize(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Check authorization during requests.
    """
    if credentials.credentials != os.getenv("BLOODTOKEN"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization code",
        )
    return credentials.credentials


@app.get("/firstbloods/all/", dependencies=[Depends(authorize)], tags=["FirstBloods"])
def read_all_firstbloods(
    update_was_sent: Optional[bool] = Query(
        False, description="Updates the was_sent value for entries"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all firstbloods in the database.
    """
    firstbloods = db.query(models.FirstBlood).all()
    if update_was_sent:
        entries_to_send = []
        for firstblood in firstbloods:
            if not firstblood.was_sent:
                data = {
                    "event_id": firstblood.event_id,
                    "challenge_id": firstblood.challenge_id,
                    "date": firstblood.date,
                    "username": firstblood.username,
                    "challenge_name": firstblood.challenge_name,
                    "challenge_category": firstblood.challenge_category,
                    "challenge_difficulty": firstblood.challenge_difficulty,
                }
                entries_to_send.append(data)
                firstblood.was_sent = True

        # Write the new entries to the sent_firstbloods table
        db.commit()
        return entries_to_send
    return firstbloods


@app.get(
    "/firstbloods/filter/", dependencies=[Depends(authorize)], tags=["FirstBloods"]
)
def read_filtered_firstbloods(
    update_was_sent: Optional[bool] = Query(
        False, description="Updates the was_sent value for entries"
    ),
    event_id: Optional[int] = Query(None, description="Event ID to filter by"),
    start_time: Optional[datetime] = Query(None, description="Start time to filter by"),
    end_time: Optional[datetime] = Query(None, description="End time to filter by"),
    challenge_id: Optional[int] = Query(None, description="Challenge ID to filter by"),
    db: Session = Depends(get_db),
):
    """
    Filter FirstBlood records by event_id, start_time, end_time, and challenge_id.

    - Time filter format is: YYYY-MM-DD HH:MM:SS
    - FirstBloods listed are descending by date.
    """
    query = db.query(models.FirstBlood)
    if event_id is not None:
        query = query.filter(models.FirstBlood.event_id == event_id)
    if start_time is not None:
        query = query.filter(models.FirstBlood.date >= start_time)
    if end_time is not None:
        query = query.filter(models.FirstBlood.date <= end_time)
    if challenge_id is not None:
        query = query.filter(models.FirstBlood.challenge_id == challenge_id)
    firstbloods = query.order_by(models.FirstBlood.date.desc()).all()

    if update_was_sent:
        entries_to_send = []
        for firstblood in firstbloods:
            if not firstblood.was_sent:
                data = {
                    "event_id": firstblood.event_id,
                    "challenge_id": firstblood.challenge_id,
                    "date": firstblood.date,
                    "username": firstblood.username,
                    "challenge_name": firstblood.challenge_name,
                    "challenge_category": firstblood.challenge_category,
                    "challenge_difficulty": firstblood.challenge_difficulty,
                }
                entries_to_send.append(data)
                firstblood.was_sent = True

        # Write the new entries to the sent_firstbloods table
        db.commit()
        return entries_to_send
    return firstbloods


@app.post("/firstbloods/add/", dependencies=[Depends(authorize)], tags=["FirstBloods"])
def create_firstblood(
    firstblood: schema.FirstBloodCreate, db: Session = Depends(get_db)
):
    """
    Create a new FirstBlood entry.

    - If date is not provided, current time is selected.
    """
    if firstblood.date is None:
        firstblood.date = datetime.now(timezone.utc)
    db_firstblood = models.FirstBlood(**dict(firstblood))
    db.add(db_firstblood)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A record with the same event_id and challenge_id already exists.",
        )
    db.refresh(db_firstblood)
    return db_firstblood
