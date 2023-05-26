"""Test routes"""

# Standard Library
import datetime
import json
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.schemas import ModelSchema
from src.prompt.constants import PromptEnum
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


settings = get_settings()


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


@pytest.mark.parametrize("alias", ["alias-1", "alias-2", "alias-3"])
@patch.object(PromptTemplateSchema, "get")
def test_get_prompt(mock_prompt_get, alias, test_client):
    """Test get prompt endpoint."""
    mock_prompt_get.return_value = [
        PromptTemplateSchema(
            template="test template",
            alias=alias,
            created_at=datetime.datetime(2022, 11, 2, 8, 34, 1),
        )
    ]
    response = test_client.get(
        f"/api/v1/prompts/{alias}", headers={"x-api-key": "1234"}
    )
    mock_prompt_get.assert_called_with(alias, raises_if_not_found=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "alias": alias,
        "created_at": "2022-11-02T08:34:01",
        "template": "test template",
        "id": None,
        "parameters": {},
        "variables": [],
        "version": 0,
    }


@pytest.mark.parametrize(
    "template, alias",
    [
        ("I want you to act like {character} from {series}.", "alias abcdefg"),
        (
            "How long does it take to become proficient in {language}",
            "alias-123456",
        ),
    ],
)
@patch("src.db.Model.save")
@patch.object(PromptTemplateSchema, "get")
def test_create_prompt(mock_prompt_get, mock_table_save, template, alias, test_client):
    """Test get prompt endpoint."""
    mock_prompt_get.return_value = None
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}",
        headers={"x-api-key": "1234"},
    )

    mock_table_save.assert_called_once()

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)
    assert isinstance(data["alias"], str)
    assert isinstance(data["version"], int)
    assert data["version"] == 0


@pytest.mark.parametrize(
    "template, alias, parameters",
    [
        (
            "Tell me a joke in {language}",
            "joke-in-different-language",
            {
                "model_name": "gpt-4",
                "max_tokens": settings.OPENAI_MAX_TOKENS,
                "temperature": settings.OPENAI_TEMPERATURE,
            },
        ),
    ],
)
@patch("src.db.Model.save")
@patch.object(PromptTemplateSchema, "get")
def test_create_prompt_with_parameters(
    mock_prompt_get, mock_table_save, template, alias, parameters, test_client
):
    """Test get prompt endpoint."""
    mock_prompt_get.return_value = None
    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}&parameters={parameters}",
        headers={"x-api-key": "1234"},
    )

    mock_table_save.assert_called_once()

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["template"], str)
    assert isinstance(data["alias"], str)
    assert isinstance(data["version"], int)
    assert isinstance(data["parameters"], dict)
    assert data["version"] == 0


@pytest.mark.parametrize(
    "template, alias, slugified_alias",
    [
        ("I want you to act like {character} from {series}.", "alias 1", "alias-1"),
    ],
)
@patch("src.db.Model.save")
@patch("src.db.Model.query")
def test_create_prompt_same_alias(
    mock_prompt_query, mock_table_save, template, alias, slugified_alias, test_client
):
    """Test get prompt endpoint."""
    mock_prompt_query.return_value = [
        PromptTemplateTable(
            id="5690d5d1-e384-4e7a-a559-4c5ad5c785a3",
            template="test-template",
            alias=slugified_alias,
            created_at=datetime.datetime(2023, 5, 22, 12, 3, 41),
        )
    ]

    response = test_client.post(
        f"/api/v1/prompts?template={template}&alias={alias}",
        headers={"x-api-key": "1234"},
    )
    data = response.json()

    mock_table_save.assert_called_once()

    assert data["version"] == 1
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    "id, template, alias, parameters, update",
    [
        (
            53463,
            "Quiero un breve resumen de dos líneas de este texto: {text}",
            "alias1",
            {},
            "I would like a brief two-line summary of this text: {text}",
        ),
        (
            "874285",
            "Quel est le framework {type} le plus populaire?",
            "alias2",
            {},
            "What's the most popular {type} framework?",
        ),
    ],
)
@patch.object(PromptTemplateSchema, "get")
@patch("src.prompt.schemas.PromptTemplateSchema.update")
def test_update_prompt(
    mock_prompt_update,
    mock_prompt_get,
    id,
    template,
    alias,
    parameters,
    update,
    test_client,
):
    """Test update prompt endpoint."""
    mock_prompt_get.return_value = [
        PromptTemplateSchema(id=id, template=template, alias=alias)
    ]
    response = test_client.put(
        f"/api/v1/prompts/{alias}?template={update}", headers={"x-api-key": "1234"}
    )
    assert mock_prompt_get.call_count == 2
    assert mock_prompt_update.call_count == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "alias": alias,
        "created_at": None,
        "id": f"{id}",
        "parameters": parameters,
        "template": template,
        "version": 0,
    }


@pytest.mark.parametrize("alias", ["alias-1", "alias-2", "alias-3"])
@patch("src.db.Model.delete")
@patch.object(PromptTemplateTable, "query")
def test_delete_prompt(
    mock_prompt_schema_query, mock_prompt_table_delete, alias, test_client
):
    """Test delete prompt endpoint."""
    mock_prompt_schema_query.return_value = [
        PromptTemplateTable(template="test template", alias=alias)
    ]

    response = test_client.delete(
        f"/api/v1/prompts/{alias}", headers={"x-api-key": "1234"}
    )

    assert mock_prompt_schema_query.call_count == 1
    mock_prompt_schema_query.assert_called_with(alias, scan_index_forward=False)
    mock_prompt_table_delete.assert_called_once()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "deleted"


@pytest.mark.parametrize(
    "alias, template", [("english-summarization", PromptEnum.EN.value[0])]
)
@patch("src.db.Model.delete")
@patch.object(PromptTemplateTable, "query")
def test_delete_prompt_protection_409(
    mock_prompt_schema_query, mock_prompt_table_delete, alias, template, test_client
):
    """Test delete prompt endpoint."""
    mock_prompt_schema_query.return_value = [
        PromptTemplateTable(template=template, alias=alias)
    ]
    response = test_client.delete(
        f"/api/v1/prompts/{alias}", headers={"x-api-key": "1234"}
    )

    mock_prompt_schema_query.assert_called_with(alias, scan_index_forward=False)
    assert mock_prompt_schema_query.call_count == 1
    assert mock_prompt_table_delete.call_count == 0

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize("alias", ["english-summarization-1"])
@patch("src.db.Model.delete")
@patch.object(PromptTemplateTable, "query")
def test_delete_prompt_protection_404(
    mock_prompt_table_query, mock_prompt_table_delete, alias, test_client
):
    """Test delete prompt endpoint."""
    mock_prompt_table_query.return_value = []
    response = test_client.delete(
        f"/api/v1/prompts/{alias}", headers={"x-api-key": "1234"}
    )

    mock_prompt_table_query.assert_called_with(alias, scan_index_forward=False)
    assert mock_prompt_table_query.call_count == 1
    assert mock_prompt_table_delete.call_count == 0

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "id, template, values, alias, parameters, generated",
    [
        (
            53463,
            "Write me a {count}-verse poem about {topic}",
            {"count": 3, "topic": "machine learning"},
            "alias1",
            None,
            "Verse 1:\nIn the world of tech, there's a buzzword we hear,\nIt's called \"machine learning,\" and it's quite clear,\nIt's a way for computers to learn and adapt,\nTo make predictions and improve how they act.\n\nVerse 2:\nFrom speech recognition to self-driving cars,\nMachine learning is taking us far,\nIt can analyze data and find patterns we miss,\nAnd help us solve problems with greater success.\n\nVerse 3:\nIt's not just for tech, it's used in many fields,\nFrom medicine to finance, it yields great yields,\nWith algorithms that can sort through the noise,\nAnd make sense of data that's vast and diverse.\n\nVerse 4:\nAs we move forward, machine learning will grow,\nAnd change how we work, live, and know,\nIt's a tool that will help us achieve,\nAnd make the impossible, possible, we believe.",  # noqa: E501
        ),
        (
            "874285",
            "What's the most popular {type} framework?",
            {"type": "web"},
            "alias2",
            "",
            "As an AI language model, I don't have access to current statistics or current trends. However, some of the most popular web frameworks currently include Angular, React, Vue.js, Django, Ruby on Rails, and Flask.",  # noqa: E501
        ),
    ],
)
@patch.object(PromptTemplateSchema, "get")
@patch("openai.ChatCompletion.create")
def test_generate_text(
    mock_openai_chat,
    mock_prompt_get,
    id,
    template,
    values,
    alias,
    parameters,
    generated,
    test_client,
):
    """Test text generation endpoint."""
    # set mock return values
    mock_openai_chat.return_value = {"choices": [{"message": {"content": generated}}]}
    mock_prompt_get.return_value = [
        PromptTemplateSchema(
            id=id, template=template, alias=alias, parameters=parameters
        )
    ]
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{alias}/generate", headers={"x-api-key": "1234"}, json=values
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
    assert response.json() == {
        "prompt": template.format(**values),
        "generated": generated,
    }


@pytest.mark.parametrize(
    "id, template, values, alias, parameters, generated",
    [
        (
            53463,
            "Write me a {count}-verse poem about {topic}",
            {"count": 3, "topic": "machine learning"},
            "alias1",
            {
                "model_name": "gpt-4",
                "max_tokens": 100,
                "temperature": 0.2,
            },
            "Verse 1:\nIn the world of tech, there's a buzzword we hear,\nIt's called \"machine learning,\" and it's quite clear,\nIt's a way for computers to learn and adapt,\nTo make predictions and improve how they act.\n\nVerse 2:\nFrom speech recognition to self-driving cars,\nMachine learning is taking us far,\nIt can analyze data and find patterns we miss,\nAnd help us solve problems with greater success.\n\nVerse 3:\nIt's not just for tech, it's used in many fields,\nFrom medicine to finance, it yields great yields,\nWith algorithms that can sort through the noise,\nAnd make sense of data that's vast and diverse.\n\nVerse 4:\nAs we move forward, machine learning will grow,\nAnd change how we work, live, and know,\nIt's a tool that will help us achieve,\nAnd make the impossible, possible, we believe.",  # noqa: E501
        )
    ],
)
@patch.object(PromptTemplateSchema, "get")
@patch("openai.ChatCompletion.create")
def test_generate_text_override_parameters(
    mock_openai_chat,
    mock_prompt_get,
    id,
    template,
    values,
    alias,
    parameters,
    generated,
    test_client,
):
    """Test text generation endpoint."""
    # set mock return values
    mock_openai_chat.return_value = {"choices": [{"message": {"content": generated}}]}
    mock_prompt_get.return_value = [
        PromptTemplateSchema(
            id=id, template=template, alias=alias, parameters=parameters
        )
    ]
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{alias}/generate", headers={"x-api-key": "1234"}, json=values
    )
    # check openai method is called
    mock_openai_chat.assert_called_with(
        model="gpt-4",
        messages=[{"role": "user", "content": template.format(**values)}],
        max_tokens=100,
        temperature=0.2,
    )

    assert mock_prompt_get.call_count == 1
    assert mock_openai_chat.call_count == 1

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "prompt": template.format(**values),
        "generated": generated,
    }


@pytest.mark.parametrize(
    "id, template, alias, model_id, model_name, values, generated",
    [
        (
            1,
            "Write me a {count}-verse poem about {topic}",
            "poem",
            2,
            "text-davinci-003",
            {"count": 3, "topic": "machine learning"},
            "Verse 1:\nIn the world of tech, there's a buzzword we hear,\nIt's called \"machine learning,\" and it's quite clear,\nIt's a way for computers to learn and adapt,\nTo make predictions and improve how they act.\n\nVerse 2:\nFrom speech recognition to self-driving cars,\nMachine learning is taking us far,\nIt can analyze data and find patterns we miss,\nAnd help us solve problems with greater success.\n\nVerse 3:\nIt's not just for tech, it's used in many fields,\nFrom medicine to finance, it yields great yields,\nWith algorithms that can sort through the noise,\nAnd make sense of data that's vast and diverse.\n\nVerse 4:\nAs we move forward, machine learning will grow,\nAnd change how we work, live, and know,\nIt's a tool that will help us achieve,\nAnd make the impossible, possible, we believe.",  # noqa: E501
        ),
        (
            "3",
            "What's the most popular {type} framework?",
            "framework",
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
    alias,
    model_id,
    model_name,
    values,
    generated,
    test_client,
):
    """Test text generation endpoint."""
    # set mock return values
    mock_openai_chat.return_value = {"choices": [{"message": {"content": generated}}]}
    mock_prompt_get.return_value = [
        PromptTemplateSchema(id=id, template=template, alias=alias)
    ]

    parameters = json.dumps(
        {
            "max_tokens": settings.OPENAI_MAX_TOKENS,
            "temperature": settings.OPENAI_TEMPERATURE,
        }
    )
    mock_model_get.return_value = ModelSchema(
        id=model_id, model_name=model_name, parameters=parameters
    )
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{alias}/generate/model/{model_name}",
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
    "id, template, alias, model_id, model_name, values",
    [
        (
            1,
            "Write me a {count}-verse poem about {topic}",
            "poem",
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
    alias,
    model_id,
    model_name,
    values,
    test_client,
):
    """Test text generation endpoint."""
    # set mock return values
    mock_prompt_get.return_value = [
        PromptTemplateSchema(id=id, template=template, alias=alias)
    ]
    parameters = json.dumps(
        {
            "max_tokens": settings.OPENAI_MAX_TOKENS,
            "temperature": settings.OPENAI_TEMPERATURE,
        }
    )
    mock_model_get.return_value = ModelSchema(
        id=model_id, model_name=model_name, parameters=parameters
    )
    # send request to test client
    response = test_client.post(
        f"/api/v1/prompts/{alias}/generate/model/{model_id}",
        headers={"x-api-key": "1234"},
        json=values,
    )

    assert mock_model_get.call_count == 1
    assert mock_prompt_get.call_count == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "generated": "Sorry, the backend for this model is in development"
    }
