# tests/api/test_products.py
def test_create_get_update_delete_product(client):
    # create
    payload = {"sku": "T-100", "name": "Test product", "price": 5.5, "stock": 10}
    r = client.post("/api/v1/products", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["sku"] == "T-100"
    pid = data["id"]

    # get
    r = client.get(f"/api/v1/products/{pid}")
    assert r.status_code == 200

    # update
    r = client.put(f"/api/v1/products/{pid}", json={"price": 6.0})
    assert r.status_code == 200
    assert r.json()["price"] == 6.0

    # delete
    r = client.delete(f"/api/v1/products/{pid}")
    assert r.status_code == 204

    # get after delete
    r = client.get(f"/api/v1/products/{pid}")
    assert r.status_code == 404