def test_stats(client):
    items = [
        {"name": "A", "price": 100},
        {"name": "B", "price": 100.56},
        {"name": "C", "price": "10.99"},
        {"name": "D", "price": 1.999999},
    ]

    for item in items:
        response = client.post(
            "/api/v1/items/add", json={"name": item["name"], "price": item["price"]}
        )

        assert response.status_code == 201

    response = client.get("/api/v1/items/stats")

    assert response.status_code == 200
    assert response.json() == {"count": len(items), "avg_price": 53.39}
