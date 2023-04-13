"""Routes test."""

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


def test_get_prompts(test_client, create_prompts):
    """Test get prompts endpoint."""
    response = test_client.get("/api/v1/prompts", headers={"x-api-key": "1234"})

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data["prompts"]) == 4


def test_get_prompt(test_client, create_prompts):
    """Test get prompt endpoint."""
    prompt = create_prompts[1]

    response = test_client.get(
        f"/api/v1/prompts/{prompt.id}", headers={"x-api-key": "1234"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == prompt.id
    assert response.json()["template"] == prompt.template
    assert response.json()["created_at"] == prompt.created_at


@pytest.mark.parametrize(
    "template",
    [
        "I want you to act like {character} from {series}."
        "What personalities are mentionned in this text {text}",
    ],
)
def test_create_prompt(template, test_client):
    """Test get prompt endpoint."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}", headers={"x-api-key": "1234"}
    )

    data = response.json()
    prompt = PromptTemplateSchema.get(id=data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)
    assert prompt.id == data["id"]
    assert prompt.created_at == data["created_at"]
    assert prompt.template == data["template"]


def test_update_prompt(test_client, create_prompts):
    """Test update prompt endpoint."""

    prompt = create_prompts[2]

    response = test_client.put(
        f"/api/v1/prompts/{prompt.id}?template=updated template",
        headers={"x-api-key": "1234"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": prompt.created_at,
        "id": prompt.id,
        "template": "updated template",
    }


def test_delete_prompt(test_client, create_prompts):
    """Test delete prompt endpoint."""

    prompt = create_prompts[3]

    response = test_client.delete(
        f"/api/v1/prompts/{prompt.id}", headers={"x-api-key": "1234"}
    )

    with pytest.raises(PromptTemplateTable.DoesNotExist):
        _ = PromptTemplateSchema.get(id=prompt.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "deleted"
