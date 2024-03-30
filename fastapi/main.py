from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException
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
def read_all_firstbloods(db: Session = Depends(get_db)):
    """
    Get all firstbloods in the database.
    """
    firstbloods = db.query(models.FirstBlood).all() 
    return firstbloods 

@app.get("/firstbloods/filter/", dependencies=[Depends(authorize)], tags=["FirstBloods"])
def read_filtered_firstbloods(event_id: Optional[int] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, challenge_id: Optional[int] = None, db: Session = Depends(get_db)):
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
    return firstbloods 

@app.post("/firstbloods/add/", dependencies=[Depends(authorize)], tags=["FirstBloods"])
def create_firstblood(firstblood: schema.FirstBloodCreate, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="A record with the same event_id and challenge_id already exists.")
    db.refresh(db_firstblood)
    return db_firstblood   
