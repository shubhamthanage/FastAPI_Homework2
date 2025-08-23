# app/schemas/payment.py
from pydantic import BaseModel

class PaymentEvent(BaseModel):
    event_id: str
    type: str
    data: dict