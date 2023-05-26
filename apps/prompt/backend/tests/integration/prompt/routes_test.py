"""Routes test."""

# Standard Library
import datetime

# 3rd party libraries
import pytest
from fastapi import status
from freezegun import freeze_time

# Source
from src.prompt.schemas import PromptTemplateSchema


def test_get_prompts(test_client, create_prompts):
    """Test get prompts endpoint."""
    response = test_client.get("/api/v1/prompts", headers={"x-api-key": "1234"})

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data["prompts"]) == 4


@freeze_time("2012-01-14 03:21:34")
def test_get_prompt(test_client, create_prompts):
    """Test get prompt endpoint."""
    prompt = create_prompts[1].dict()

    response = test_client.get(
        f"/api/v1/prompts/{prompt['alias']}", headers={"x-api-key": "1234"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == prompt["id"]
    assert response.json()["template"] == prompt["template"]
    assert (
        datetime.datetime.fromisoformat(response.json()["created_at"])
        == prompt["created_at"]
    )
    assert response.json()["alias"] == prompt["alias"]


@pytest.mark.parametrize(
    "template, alias, parameters",
    [
        ("I want you to act like {character} from {series}.", "aliasone", ""),
        (
            "What personalities are mentionned in this text {text}",
            "aliastwo",
            {
                "model_name": "gpt-4",
                "max_tokens": 100,
                "temperature": 0.2,
            },
        ),
    ],
)
@freeze_time("2012-01-14 03:21:34")
def test_create_prompt(template, test_client, alias, parameters):
    """Test create prompt endpoint."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}&parameters={parameters}",
        headers={"x-api-key": "1234"},
    )

    data = response.json()
    prompt = PromptTemplateSchema.get(alias=data["alias"])[0]

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)
    assert isinstance(data["alias"], str)
    assert isinstance(data["parameters"], dict)
    assert prompt.id == data["id"]
    assert prompt.created_at == datetime.datetime.fromisoformat(data["created_at"])
    assert prompt.template == data["template"]
    assert prompt.alias == data["alias"]
    assert prompt.parameters == data["parameters"]


@pytest.mark.parametrize(
    "template, alias",
    [
        (
            "template-x",
            "t1",
        ),
    ],
)
def test_create_prompt_same_alias(test_client, template, alias):
    """Test create prompt endpoint with alias in database."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}",
        headers={"x-api-key": "1234"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["version"] == 1


def test_update_prompt(test_client, create_prompts):
    """Test update prompt endpoint."""
    prompt = create_prompts[2]
    response = test_client.put(
        f"/api/v1/prompts/{prompt.alias}?template=updated template",
        headers={"x-api-key": "1234"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["template"] == "updated template"
    assert response.json()["alias"] == prompt.alias
    assert response.json()["version"] == 1


@pytest.mark.parametrize(
    "alias",
    ["t1", "t2"],
)
def test_delete_prompt(test_client, alias):
    """Test delete prompt endpoint."""

    response = test_client.delete(
        f"/api/v1/prompts/{alias}", headers={"x-api-key": "1234"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "deleted"


# TODO: add integration tests for generate endpoints
