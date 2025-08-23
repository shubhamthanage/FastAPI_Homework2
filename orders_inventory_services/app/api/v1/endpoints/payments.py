# app/api/v1/endpoints/payments.py
import hmac
import hashlib
import json
from fastapi import APIRouter, Request, Header, HTTPException, status, Depends
from sqlmodel import Session
from app.core.config import settings
from app.services.payment_service import handle_payment_event
from app.db.session import get_session

router = APIRouter()

SIGNATURE_HEADER = "X-Signature"  # chosen header for HMAC-SHA256 hex digest

@router.post("/payment")
async def payment_webhook(request: Request, x_signature: str | None = Header(None), session: Session = Depends(get_session)):
    # read raw body for HMAC calculation
    raw_body = await request.body()
    if x_signature is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature header")

    computed = hmac.new(settings.WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    # constant-time compare
    if not hmac.compare_digest(computed, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")

    # process event (idempotent & checks replay)
    try:
        handle_payment_event(session, payload)
    except ValueError as e:
        # e.g., replay or unknown order
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"status": "ok"}