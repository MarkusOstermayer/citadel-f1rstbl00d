# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # import your Base

DATABASE_URL = "sqlite:///./bloodcount.db"  # Use your actual database URL here

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This will create all tables that don't exist yet.
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()