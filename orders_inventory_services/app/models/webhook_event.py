# app/models/webhook_event.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String

class WebhookEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(sa_column=Column("event_id", String, unique=True, index=True), nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)