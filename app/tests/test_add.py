def test_right_item_add(client):
    response = client.post("/api/v1/items/add", json={"name": "A", "price": 1})

    assert response.status_code == 201


def test_wrong_name(client):
    response = client.post("/api/v1/items/add", json={"name": "", "price": 1})

    assert response.status_code == 400


def test_wrong_price(client):
    response = client.post("/api/v1/items/add", json={"name": "A", "price": -1})

    assert response.status_code == 400
