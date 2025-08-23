# Orders & Inventory Service

Run locally:
- Create venv and install: pip install -r requirements.txt
- Start: uvicorn app.main:app --reload

API base: http://127.0.0.1:8000/api/v1
Docs: http://127.0.0.1:8000/docs

Key endpoints:
- POST /api/v1/products -> 201 or 409 if SKU exists
- GET /api/v1/products
- GET /api/v1/products/{id} -> 404 if not found
- PUT /api/v1/products/{id} -> full/partial updates allowed (PATCH-like via fields)
- DELETE /api/v1/products/{id} -> 204

- POST /api/v1/orders -> 201; atomically reduces stock, returns 409 on insufficient stock
- GET /api/v1/orders/{id}
- PUT /api/v1/orders/{id} -> change status or quantity (quantity only when PENDING)
- DELETE /api/v1/orders/{id} -> allowed only if PENDING

Webhook:
- POST /api/v1/webhooks/payment
  - Header X-Signature: hex HMAC-SHA256 of body using WEBHOOK_SECRET
  - Payload: {"event_id": "...", "type": "payment.succeeded", "data":{"order_id": 1}}
  - Idempotent and protects against replay via stored event_id

Error shapes:
- {"detail": "Insufficient stock"} or descriptive messages.

Tests:
- pytest runs unit tests using TestClient.

Notes on concurrency:
- SQLite is limited for concurrent writes. Production: use Postgres with row-level locking or SELECT ... FOR UPDATE.
 