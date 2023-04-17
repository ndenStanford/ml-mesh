"""Test routes.x"""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.schemas import ModelSchema
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


@patch.object(PromptTemplateSchema, "get")
def test_get_prompts(mock_prompt_get, test_client):
    """Test get prompts endpoint."""
    mock_prompt_get.return_value = []
    response = test_client.get("/api/v1/prompts", headers={"x-api-key": "1234"})
    mock_prompt_get.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"prompts": []}


def test_get_prompts_unauthenticated(test_client):
    """Test get prompts endpoint unauthenticated."""
    response = test_client.get("/api/v1/prompts")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("id", [1, 124543, "2423"])
@patch.object(PromptTemplateSchema, "get")
def test_get_prompt(mock_prompt_get, id, test_client):
    """Test get prompt endpoint."""
    mock_prompt_get.return_value = PromptTemplateSchema(id=id, template="test template")
    response = test_client.get(f"/api/v1/prompts/{id}", headers={"x-api-key": "1234"})
    mock_prompt_get.assert_called_with(f"{id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": None,
        "id": f"{id}",
        "template": "test template",
    }


def test_get_prompt_unauthenticated(test_client):
    """Test get prompt endpoint unauthenticated."""
    response = test_client.get("/api/v1/prompts/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "id, template",
    [
        (53463, "I want you to act like {character} from {series}."),
        (
            "874285",
            "How long does it take to become proficient in {language}",
        ),
    ],
)
@patch("src.db.Model.save")
def test_create_prompt(mock_table_save, id, template, test_client):
    """Test get prompt endpoint."""
    response = test_client.post(
        f"/api/v1/prompts?template={template}", headers={"x-api-key": "1234"}
    )

    mock_table_save.assert_called_once()

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)


def test_create_prompt_unauthenticated(test_client):
    """Test create prompt endpoint unauthenticated."""
    response = test_client.post("/api/v1/prompts?template=template")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "id, template, update",
    [
        (
            53463,
            "Quiero un breve resumen de dos líneas de este texto: {text}",
            "I would like a brief two-line summary of this text: {text}",
        ),
        (
            "874285",
            "Quel est le framework {type} le plus populaire?",
            "What's the most popular {type} framework?",
        ),
    ],
)
@patch.object(PromptTemplateSchema, "get")
@patch("src.prompt.schemas.PromptTemplateSchema.update")
def test_update_prompt(
    mock_prompt_update, mock_prompt_get, id, template, update, test_client
):
    """Test update prompt endpoint."""
    mock_prompt_get.return_value = PromptTemplateSchema(id=id, template=template)
    response = test_client.put(
        f"/api/v1/prompts/{id}?template={update}", headers={"x-api-key": "1234"}
    )
    assert mock_prompt_get.call_count == 2
    assert mock_prompt_update.call_count == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"created_at": None, "id": f"{id}", "template": template}


def test_update_prompt_unauthenticated(test_client):
    """Test update prompt endpoint unauthenticated."""
    response = test_client.put("/api/v1/prompts/12345?template=template")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("id", [1, 124543, "2423"])
@patch.object(PromptTemplateTable, "get")
@patch("src.prompt.tables.PromptTemplateTable.delete")
def test_delete_prompt(mock_prompt_delete, mock_prompt_get, id, test_client):
    """Test delete prompt endpoint."""
    mock_prompt_get.return_value = PromptTemplateTable(id=id, template="test template")

    response = test_client.delete(
        f"/api/v1/prompts/{id}", headers={"x-api-key": "1234"}
    )

    assert mock_prompt_get.call_count == 1
    assert mock_prompt_delete.call_count == 1

    mock_prompt_get.assert_called_with(f"{id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "deleted"


def test_delete_prompt_unauthenticated(test_client):
    """Test delete prompt endpoint unauthenticated."""
    response = test_client.delete("/api/v1/prompts/12345")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "id, template, values, generated",
    [
        (
            53463,
            "Write me a {count}-verse poem about {topic}",
            {"count": 3, "topic": "machine learning"},
            "Verse 1:\nIn the world of tech, there's a buzzword we hear,\nIt's called \"machine learning,\" and it's quite clear,\nIt's a way for computers to learn and adapt,\nTo make predictions and improve how they act.\n\nVerse 2:\nFrom speech recognition to self-driving cars,\nMachine learning is taking us far,\nIt can analyze data and find patterns we miss,\nAnd help us solve problems with greater success.\n\nVerse 3:\nIt's not just for tech, it's used in many fields,\nFrom medicine to finance, it yields great yields,\nWith algorithms that can sort through the noise,\nAnd make sense of data that's vast and diverse.\n\nVerse 4:\nAs we move forward, machine learning will grow,\nAnd change how we work, live, and know,\nIt's a tool that will help us achieve,\nAnd make the impossible, possible, we believe.",  # noqa: E501
        ),
        (
            "874285",
            "What's the most popular {type} framework?",
            {"type": "web"},
            "As an AI language model, I don't have access to current statistics or current trends. However, some of the most popular web frameworks currently include Angular, React, Vue.js, Django, Ruby on Rails, and Flask.",  # noqa: E501
        ),
    ],
)
@patch.object(PromptTemplateSchema, "get")
@patch("openai.ChatCompletion.create")
def test_generate_text(
    mock_openai_chat, mock_prompt_get, id, template, values, generated, test_client
):
    """Test text generation endpoint."""
    settings = get_settings()
    # set mock return values
    mock_openai_chat.return_value = {"choices": [{"message": {"content": generated}}]}
    mock_prompt_get.return_value = PromptTemplateSchema(id=id, template=template)
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{id}/generate", headers={"x-api-key": "1234"}, json=values
    )
    # check openai method is called
    mock_openai_chat.assert_called_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": template.format(**values)}],
        max_tokens=settings.OPENAI_MAX_TOKENS,
        temperature=settings.OPENAI_TEMPERATURE,
    )

    assert mock_prompt_get.call_count == 1
    assert mock_openai_chat.call_count == 1

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"generated": generated}


@pytest.mark.parametrize(
    "id, template, model_id, model_name, values, generated",
    [
        (
            1,
            "Write me a {count}-verse poem about {topic}",
            2,
            "text-davinci-003",
            {"count": 3, "topic": "machine learning"},
            "Verse 1:\nIn the world of tech, there's a buzzword we hear,\nIt's called \"machine learning,\" and it's quite clear,\nIt's a way for computers to learn and adapt,\nTo make predictions and improve how they act.\n\nVerse 2:\nFrom speech recognition to self-driving cars,\nMachine learning is taking us far,\nIt can analyze data and find patterns we miss,\nAnd help us solve problems with greater success.\n\nVerse 3:\nIt's not just for tech, it's used in many fields,\nFrom medicine to finance, it yields great yields,\nWith algorithms that can sort through the noise,\nAnd make sense of data that's vast and diverse.\n\nVerse 4:\nAs we move forward, machine learning will grow,\nAnd change how we work, live, and know,\nIt's a tool that will help us achieve,\nAnd make the impossible, possible, we believe.",  # noqa: E501
        ),
        (
            "3",
            "What's the most popular {type} framework?",
            "4",
            "text-curie-001",
            {"type": "web"},
            "As an AI language model, I don't have access to current statistics or current trends. However, some of the most popular web frameworks currently include Angular, React, Vue.js, Django, Ruby on Rails, and Flask.",  # noqa: E501
        ),
    ],
)
@patch.object(ModelSchema, "get")
@patch.object(PromptTemplateSchema, "get")
@patch("openai.ChatCompletion.create")
def test_generate_text_with_diff_model(
    mock_openai_chat,
    mock_prompt_get,
    mock_model_get,
    id,
    template,
    model_id,
    model_name,
    values,
    generated,
    test_client,
):
    """Test text generation endpoint."""
    settings = get_settings()
    # set mock return values
    mock_openai_chat.return_value = {"choices": [{"message": {"content": generated}}]}
    mock_prompt_get.return_value = PromptTemplateSchema(id=id, template=template)
    mock_model_get.return_value = ModelSchema(id=model_id, model_name=model_name)
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{id}/generate/model/{model_id}",
        headers={"x-api-key": "1234"},
        json=values,
    )
    # check openai method is called
    mock_openai_chat.assert_called_with(
        model=model_name,
        messages=[{"role": "user", "content": template.format(**values)}],
        max_tokens=settings.OPENAI_MAX_TOKENS,
        temperature=settings.OPENAI_TEMPERATURE,
    )

    assert mock_model_get.call_count == 1
    assert mock_prompt_get.call_count == 1
    assert mock_openai_chat.call_count == 1

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"generated": generated}


@pytest.mark.parametrize(
    "id, template, model_id, model_name, values",
    [
        (
            1,
            "Write me a {count}-verse poem about {topic}",
            2,
            "model-x",
            {"count": 3, "topic": "machine learning"},
        ),
    ],
)
@patch.object(ModelSchema, "get")
@patch.object(PromptTemplateSchema, "get")
def test_generate_text_with_diff_model_model_not_found(
    mock_prompt_get,
    mock_model_get,
    id,
    template,
    model_id,
    model_name,
    values,
    test_client,
):
    """Test text generation endpoint."""
    # set mock return values
    mock_prompt_get.return_value = PromptTemplateSchema(id=id, template=template)
    mock_model_get.return_value = ModelSchema(id=model_id, model_name=model_name)
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{id}/generate/model/{model_id}",
        headers={"x-api-key": "1234"},
        json=values,
    )

    assert mock_model_get.call_count == 1
    assert mock_prompt_get.call_count == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "generated": "Sorry, the backend for this model is in development"
    }


def test_generate_unauthenticated(test_client):
    """Test generate endpoint unauthenticated."""
    response = test_client.post("/api/v1/prompts/1/generate")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


def test_generate_with_diff_model_unauthenticated(test_client):
    """Test generate endpoint unauthenticated."""
    response = test_client.post("/api/v1/prompts/1/generate/model/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
