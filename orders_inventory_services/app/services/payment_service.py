# app/services/payment_service.py
from sqlmodel import Session, select
from orders_inventory_services.app.models.order import Order, OrderStatus
from orders_inventory_services.app.models.webhook_event import WebhookEvent
from datetime import datetime

def handle_payment_event(session: Session, payload: dict):
    # Expect payload like: {"event_id": "evt_1", "type": "payment.succeeded", "data": {"order_id": 1}}
    event_id = payload.get("event_id")
    if not event_id:
        raise ValueError("Missing event_id")
    # replay protection: unique event_id in WebhookEvent table
    existing = session.exec(select(WebhookEvent).where(WebhookEvent.event_id == event_id)).first()
    if existing:
        raise ValueError("Event already processed")
    # mark event as processed (to prevent race: add before processing order state change)
    evt = WebhookEvent(event_id=event_id)
    session.add(evt)
    session.commit()  # commit to persist seen event
    # process event
    typ = payload.get("type")
    if typ == "payment.succeeded":
        data = payload.get("data", {})
        order_id = data.get("order_id")
        if order_id is None:
            raise ValueError("Missing order_id in event data")
        order = session.get(Order, order_id)
        if not order:
            raise ValueError("Order not found")
        # only apply if pending
        if order.status == OrderStatus.PAID:
            return  # idempotent - already paid, just return success
        if order.status != OrderStatus.PENDING:
            # allow marking PAID only from PENDING
            raise ValueError("Order is not in PENDING and cannot be marked PAID")
        order.status = OrderStatus.PAID
        session.add(order)
        session.commit()
        return
    else:
        # we only support succeeded payment in this service
        raise ValueError("Unsupported event type")