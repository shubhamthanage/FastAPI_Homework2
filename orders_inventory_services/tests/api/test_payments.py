# tests/api/test_payments.py
import hmac, hashlib, json
from app.core.config import settings

def sign(body: bytes) -> str:
    return hmac.new(settings.WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()

def test_payment_webhook(client):
    # create product & order
    p = {"sku": "PAY-1", "name": "Pay prod", "price": 3.0, "stock": 2}
    r = client.post("/api/v1/products", json=p)
    product = r.json()
    pid = product["id"]

    o = {"product_id": pid, "quantity": 1}
    r = client.post("/api/v1/orders", json=o)
    order = r.json()
    oid = order["id"]

    # valid payment event
    event = {"event_id": "evt-pay-1", "type": "payment.succeeded", "data": {"order_id": oid}}
    body = json.dumps(event).encode()
    headers = {"X-Signature": sign(body)}
    r = client.post("/api/v1/webhooks/payment", data=body, headers=headers)
    assert r.status_code == 200

    # calling again should be rejected as replay
    r = client.post("/api/v1/webhooks/payment", data=body, headers=headers)
    assert r.status_code == 400

    # invalid signature returns 401
    headers = {"X-Signature": "bad-sign"}
    r = client.post("/api/v1/webhooks/payment", data=body, headers=headers)
    assert r.status_code == 401