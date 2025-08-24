# app/api/v1/endpoints/payments.py
import hmac
import hashlib
import json
import uuid
from fastapi import APIRouter, Request, Header, HTTPException, status, Depends
from sqlmodel import Session
from app.core.config import settings
from app.services.payment_service import handle_payment_event
from app.db.session import get_session
from app.schemas.payment import PaymentRequest, PaymentResponse, SignatureRequest, SignatureResponse

router = APIRouter()

SIGNATURE_HEADER = "X-Signature"  # chosen header for HMAC-SHA256 hex digest

@router.post("/payment", response_model=PaymentResponse)
async def payment_webhook(
    payment_data: PaymentRequest,
    request: Request, 
    x_signature: str | None = Header(None), 
    session: Session = Depends(get_session)
):
    if x_signature is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature header")

    # Use the same signature computation method as generate-signature endpoint
    # Convert the validated data to JSON string, then to bytes
    json_string = payment_data.model_dump_json()
    json_bytes = json_string.encode('utf-8')
    
    computed = hmac.new(settings.WEBHOOK_SECRET.encode(), json_bytes, hashlib.sha256).hexdigest()
    
    # constant-time compare
    if not hmac.compare_digest(computed, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        # Convert the validated data to dict for processing
        payment_payload = payment_data.model_dump()
        
        # Transform payment data into webhook event format expected by handle_payment_event
        webhook_event = {
            "event_id": f"evt_{uuid.uuid4().hex[:8]}",  # Generate unique event ID
            "type": "payment.succeeded",
            "data": {
                "order_id": int(payment_payload["order_id"]),  # Convert to int as expected by service
                "amount": float(payment_payload["amount"]),
                "currency": payment_payload["currency"],
                "payment_method": payment_payload["payment_method"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data: {str(e)}")

    # process event (idempotent & checks replay)
    try:
        handle_payment_event(session, webhook_event)
    except ValueError as e:
        # e.g., replay or unknown order
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return PaymentResponse(status="ok", message="Payment processed successfully")

@router.post("/generate-signature", response_model=SignatureResponse)
async def generate_signature(signature_request: SignatureRequest):
    """
    Generate HMAC-SHA256 signature for payment data.
    This endpoint helps with testing by generating the required x-signature header.
    """
    # Convert the request to JSON string, then to bytes
    json_string = signature_request.model_dump_json()
    json_bytes = json_string.encode('utf-8')
    
    # Compute HMAC-SHA256 signature
    signature = hmac.new(
        settings.WEBHOOK_SECRET.encode('utf-8'),
        json_bytes,
        hashlib.sha256
    ).hexdigest()
    
    return SignatureResponse(
        signature=signature,
        payload=signature_request.model_dump()
    )