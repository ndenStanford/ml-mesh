"""Schemas test."""

# Standard Library
import json
from datetime import datetime, timezone
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable
from src.settings import get_settings


settings = get_settings()


@pytest.mark.parametrize(
    "model_name, max_tokens, temperature",
    [
        ("text-davinci-003", settings.OPENAI_MAX_TOKENS, settings.OPENAI_TEMPERATURE),
        ("text-curie-001", settings.OPENAI_MAX_TOKENS, settings.OPENAI_TEMPERATURE),
    ],
)
@patch("src.db.Model.save")
def test_init_model_name_schema(mock_save, model_name, max_tokens, temperature):
    """Assert model initialization."""
    parameters = json.dumps({"max_tokens": max_tokens, "temperature": temperature})

    model = ModelSchema(model_name=model_name, parameters=parameters)

    assert model.model_name == model_name
    assert json.loads(model.parameters)["max_tokens"] == settings.OPENAI_MAX_TOKENS
    assert json.loads(model.parameters)["temperature"] == settings.OPENAI_TEMPERATURE
    # values only assigned when saved in database
    assert model.id is None
    assert model.created_at is None


@pytest.mark.parametrize(
    "model_name, max_tokens, temperature",
    [
        ("text-davinci-003", settings.OPENAI_MAX_TOKENS, settings.OPENAI_TEMPERATURE),
        ("text-curie-001", settings.OPENAI_MAX_TOKENS, settings.OPENAI_TEMPERATURE),
    ],
)
@patch("src.db.Model.save")
def test_save_model_schema(mock_save, model_name, max_tokens, temperature):
    """Assert model initialization."""
    parameters = json.dumps({"max_tokens": max_tokens, "temperature": temperature})
    model_name = ModelSchema(model_name=model_name, parameters=parameters)
    saved_model_name = model_name.save()

    mock_save.assert_called_once()

    assert isinstance(saved_model_name.id, str)
    assert isinstance(saved_model_name.created_at, datetime)
    assert isinstance(saved_model_name.model_name, str)
    assert isinstance(saved_model_name.parameters, str)


@pytest.mark.parametrize(
    "id",
    ["39ba8bf2-3a40-42a2-9ca1-27fa3de39e2b", "69095223-dae8-47ad-a077-150e5c5986db"],
)
@patch.object(ModelTable, "query")
def test_get_model_properties_schema_with_id(mock_get, id):
    """Test retrieve model properties with id."""
    mock_get.return_value = [
        ModelTable(
            id=id,
            model_name="model_name",
            parameters=json.dumps(
                {
                    "max_tokens": settings.OPENAI_MAX_TOKENS,
                    "temperature": settings.OPENAI_TEMPERATURE,
                }
            ),
            created_at=datetime.now(timezone.utc),
        )
    ]
    _ = ModelSchema.get(id)
    mock_get.assert_called_with(id)
