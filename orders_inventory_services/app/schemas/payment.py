# app/schemas/payment.py
from pydantic import BaseModel
from decimal import Decimal

class PaymentEvent(BaseModel):
    event_id: str
    type: str
    data: dict

class PaymentRequest(BaseModel):
    amount: Decimal
    currency: str
    order_id: str
    payment_method: str

class PaymentResponse(BaseModel):
    status: str
    message: str

class SignatureRequest(BaseModel):
    amount: Decimal
    currency: str
    order_id: str
    payment_method: str

class SignatureResponse(BaseModel):
    signature: str
    payload: dict