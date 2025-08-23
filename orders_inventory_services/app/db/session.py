# app/db/session.py
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from typing import Generator

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session