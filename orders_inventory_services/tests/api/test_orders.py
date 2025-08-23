# tests/api/test_orders.py
def test_order_flow(client):
    # create product
    p = {"sku": "ORD-1", "name": "For order", "price": 2.0, "stock": 5}
    r = client.post("/api/v1/products", json=p)
    assert r.status_code == 201
    product = r.json()
    pid = product["id"]

    # create order
    o = {"product_id": pid, "quantity": 3}
    r = client.post("/api/v1/orders", json=o)
    assert r.status_code == 201
    order = r.json()
    oid = order["id"]
    assert order["quantity"] == 3
    assert order["status"] == "PENDING"

    # try increase quantity beyond stock
    r = client.put(f"/api/v1/orders/{oid}", json={"quantity": 5})
    assert r.status_code == 409 or r.status_code == 400

    # cancel order
    r = client.put(f"/api/v1/orders/{oid}", json={"status": "CANCELED"})
    assert r.status_code == 200
    assert r.json()["status"] == "CANCELED"