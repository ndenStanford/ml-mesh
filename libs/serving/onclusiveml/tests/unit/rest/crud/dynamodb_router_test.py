"""Test DynamoDB router."""

# Standard Library
from http import HTTPStatus


def test_create_item(client):
    """Test creating a new item."""
    response = client.post("/items", json={"name": "Alice", "age": 30})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Alice"
    assert data["age"] == 30
    assert "id" in data


def test_create_item_missing_required_field(client):
    """Test creating an item without required fields."""
    response = client.post("/items", json={"age": 25})  # Missing 'name'
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_items(client):
    """Test retrieving all items."""
    # Create multiple items
    items = [
        {"name": "Bob", "age": 40},
        {"name": "Charlie", "age": 22},
        {"name": "Diana", "age": 28},
    ]
    for item in items:
        client.post("/items", json=item)

    response = client.get("/items")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 3
    names = [item["name"] for item in data]
    assert "Bob" in names
    assert "Charlie" in names
    assert "Diana" in names


def test_get_one_existing_item(client):
    """Test retrieving an existing item by ID."""
    # Create an item
    response = client.post("/items", json={"name": "Eve", "age": 35})
    item_id = response.json()["id"]
    # Retrieve the item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Eve"
    assert data["age"] == 35
    assert data["id"] == item_id


def test_get_one_nonexistent_item(client):
    """Test retrieving a non-existent item."""
    response = client.get("/items/nonexistent-id")
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id not found in database"


def test_update_existing_item(client):
    """Test updating an existing item."""
    # Create an item
    response = client.post("/items", json={"name": "Frank", "age": 45})
    item_id = response.json()["id"]
    # Update the item
    update_data = {"name": "Franklin", "age": 46}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Franklin"
    assert data["age"] == 46
    assert data["id"] == item_id


def test_update_nonexistent_item(client):
    """Test updating a non-existent item."""
    update_data = {"name": "Grace", "age": 50}
    response = client.put("/items/nonexistent-id", json=update_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id not found in database"


def test_delete_existing_item(client):
    """Test deleting an existing item."""
    # Create an item
    response = client.post("/items", json={"name": "Heidi", "age": 29})
    item_id = response.json()["id"]
    # Delete the item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Heidi"
    # Verify the item is deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item."""
    response = client.delete("/items/nonexistent-id")
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id not found in database"


def test_delete_all_items(client):
    """Test deleting all items."""
    # Create multiple items
    items = [
        {"name": "Ivan", "age": 31},
        {"name": "Judy", "age": 27},
    ]
    for item in items:
        client.post("/items", json=item)
    # Delete all items
    response = client.delete("/items")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 2
    # Verify all items are deleted
    response = client.get("/items")
    data = response.json()
    assert len(data) == 0


def test_pagination(client):
    """Test pagination parameters in get all items."""
    # Create multiple items
    for i in range(10):
        client.post("/items", json={"name": f"User{i}", "age": 20 + i})
    # Retrieve items with pagination
    response = client.get("/items?skip=1&limit=3")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 3


def test_create_item_invalid_input(client):
    """Test creating an item with invalid input."""
    response = client.post("/items", json={"name": 123, "age": "abc"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_item_invalid_input(client):
    """Test updating an item with invalid input."""
    # Create an item
    response = client.post("/items", json={"name": "Laura", "age": 24})
    item_id = response.json()["id"]
    # Update with invalid data
    response = client.put(f"/items/{item_id}", json={"name": 456})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_items_empty(client):
    """Test retrieving all items when none exist."""
    response = client.get("/items")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []


def test_delete_all_items_empty(client):
    """Test deleting all items when none exist."""
    response = client.delete("/items")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []


def test_partial_update(client):
    """Test partial update of an item."""
    # Create an item
    response = client.post("/items", json={"name": "Mallory", "age": 26})
    item_id = response.json()["id"]
    # Partial update (only age)
    update_data = {"age": 27}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Mallory"
    assert data["age"] == 27


def test_extra_fields_in_create(client):
    """Test creating an item with extra fields."""
    response = client.post("/items", json={"name": "Nina", "age": 30, "extra": "field"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_extra_fields_in_update(client):
    """Test updating an item with extra fields."""
    # Create an item
    response = client.post("/items", json={"name": "Oscar", "age": 32})
    assert response.status_code == HTTPStatus.OK
    item_id = response.json()["id"]
    # Update with extra field
    response = client.put(f"/items/{item_id}", json={"extra": "field"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_items_with_invalid_pagination(client):
    """Test retrieving items with invalid pagination parameters."""
    response = client.get("/items?skip=-1&limit=0")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
