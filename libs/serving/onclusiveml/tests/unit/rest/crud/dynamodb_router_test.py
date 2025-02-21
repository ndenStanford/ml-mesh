"""Test DynamoDB router."""

# Standard Library
import json
from http import HTTPStatus


def test_create_item(client):
    """Test creating a new item."""
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Alice", "age": 30}
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Alice"
    assert data["age"] == 30
    assert "id" in data


def test_create_item_missing_required_field(client):
    """Test creating an item without required fields."""
    response = client.post(
        "/test-service/v1/test_table", json={"age": 25}
    )  # Missing 'name'
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
        client.post("/test-service/v1/test_table", json=item)

    response = client.get("/test-service/v1/test_table")
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
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Eve", "age": 35}
    )
    item_id = response.json()["id"]
    # Retrieve the item
    response = client.get(f"/test-service/v1/test_table/{item_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Eve"
    assert data["age"] == 35
    assert data["id"] == item_id


def test_get_one_nonexistent_item(client):
    """Test retrieving a non-existent item."""
    response = client.get("/test-service/v1/test_table/nonexistent-id")
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id does not exist."


def test_update_existing_item(client):
    """Test updating an existing item."""
    # Create an item
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Frank", "age": 45}
    )
    item_id = response.json()["id"]
    # Update the item
    update_data = {"name": "Franklin", "age": 46}
    response = client.put(f"/test-service/v1/test_table/{item_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Franklin"
    assert data["age"] == 46
    assert data["id"] == item_id


def test_update_nonexistent_item(client):
    """Test updating a non-existent item."""
    update_data = {"name": "Grace", "age": 50}
    response = client.put(
        "/test-service/v1/test_table/nonexistent-id", json=update_data
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id does not exist."


def test_delete_existing_item(client):
    """Test deleting an existing item."""
    # Create an item
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Heidi", "age": 29}
    )
    item_id = response.json()["id"]
    # Delete the item
    response = client.delete(f"/test-service/v1/test_table/{item_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Heidi"
    # Verify the item is deleted
    response = client.get(f"/test-service/v1/test_table/{item_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item."""
    response = client.delete("/test-service/v1/test_table/nonexistent-id")
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"] == "Item with id nonexistent-id does not exist."


def test_delete_all_items(client):
    """Test deleting all items."""
    # Create multiple items
    items = [
        {"name": "Ivan", "age": 31},
        {"name": "Judy", "age": 27},
    ]
    for item in items:
        client.post("/test-service/v1/test_table", json=item)
    # Delete all items
    response = client.delete("/test-service/v1/test_table")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 2
    # Verify all items are deleted
    response = client.get("/test-service/v1/test_table")
    data = response.json()
    assert len(data) == 0


def test_create_item_invalid_input(client):
    """Test creating an item with invalid input."""
    response = client.post(
        "/test-service/v1/test_table", json={"name": 123, "age": "abc"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_item_invalid_input(client):
    """Test updating an item with invalid input."""
    # Create an item
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Laura", "age": 24}
    )
    item_id = response.json()["id"]
    # Update with invalid data
    response = client.put(f"/test-service/v1/test_table/{item_id}", json={"name": 456})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_items_empty(client):
    """Test retrieving all items when none exist."""
    response = client.get("/test-service/v1/test_table")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []


def test_delete_all_items_empty(client):
    """Test deleting all items when none exist."""
    response = client.delete("/test-service/v1/test_table")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == []


def test_partial_update(client):
    """Test partial update of an item."""
    # Create an item
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Mallory", "age": 26}
    )
    item_id = response.json()["id"]
    # Partial update (only age)
    update_data = {"age": 27}
    response = client.put(f"/test-service/v1/test_table/{item_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == "Mallory"
    assert data["age"] == 27


def test_extra_fields_in_create(client):
    """Test creating an item with extra fields."""
    response = client.post(
        "/test-service/v1/test_table",
        json={"name": "Nina", "age": 30, "extra": "field"},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_extra_fields_in_update(client):
    """Test updating an item with extra fields."""
    # Create an item
    response = client.post(
        "/test-service/v1/test_table", json={"name": "Oscar", "age": 32}
    )
    assert response.status_code == HTTPStatus.OK
    item_id = response.json()["id"]
    # Update with extra field
    response = client.put(
        f"/test-service/v1/test_table/{item_id}", json={"extra": "field"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_query(client):
    """Test get item via search query."""
    # Create multiple items
    items = [
        {"name": "Name1", "age": 25},
        {"name": "Name2", "age": 20},
        {"name": "Name2", "age": 26},
        {"name": "Name2", "age": 27},
        {"name": "Name2", "age": 35},
    ]
    for item in items:
        client.post("/test-service/v1/test_table", json=item)
    # test search query
    condition_str = 'A("name").eq("Name2")'
    age_condition_1 = 'A("age")<30'
    age_condition_2 = 'A("age")>25'
    age_condition = age_condition_1 + " & " + age_condition_2
    db_query = {
        "hash_key": condition_str,
        "filter_condition": age_condition,
        "index": "name-index",
    }
    serialized_query = json.dumps(db_query)

    response = client.get(
        "/test-service/v1/test_table/query",
        params={"serialized_query": serialized_query},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
