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
    assert response.json()["alias"] == prompt.alias


@pytest.mark.parametrize(
    "template, alias",
    [
        (
            "I want you to act like {character} from {series}.",
            "alias1",
        ),
        (
            "What personalities are mentionned in this text {text}",
            "alias2",
        ),
    ],
)
def test_create_prompt(template, test_client, alias):
    """Test create prompt endpoint."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}",
        headers={"x-api-key": "1234"},
    )

    data = response.json()
    prompt = PromptTemplateSchema.get(id=data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)
    assert isinstance(data["alias"], str)
    assert prompt.id == data["id"]
    assert prompt.created_at == data["created_at"]
    assert prompt.template == data["template"]
    assert prompt.alias == data["alias"]


@pytest.mark.parametrize(
    "template, alias",
    [
        (
            "template-x",
            "t1",
        ),
    ],
)
def test_create_prompt_same_alias(test_client, create_prompts, template, alias):
    """Test create prompt endpoint with alias in database."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}",
        headers={"x-api-key": "1234"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "{} already exists in the database, please provide a unique alias".format(
            alias
        )
    }


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
        "alias": prompt.alias,
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
