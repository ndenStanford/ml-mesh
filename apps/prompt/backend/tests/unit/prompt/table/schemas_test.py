"""Schemas test."""

# Standard Library
from datetime import datetime, timezone
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


@pytest.mark.parametrize(
    "template, alias",
    [
        ("What are the main topics discussed in this text: {text}.", "alias1"),
        ("Peux-tu resumer en {count} mots cet article: {text}?", "alias2"),
    ],
)
@patch("src.db.Model.save")
def test_init_prompt_template_schema(mock_save, template, alias):
    """Assert prompt initialization"""
    prompt = PromptTemplateSchema(template=template, alias=alias)

    assert prompt.template == template
    assert prompt.alias == alias
    # values only assigned when saved in database
    assert prompt.id is None
    assert prompt.created_at is None


@pytest.mark.parametrize(
    "template, variables, alias",
    [
        (
            "What are the main topics discussed in this text: {text}.",
            ["text"],
            "alias1",
        ),
        (
            "Peux-tu resumer en {count} mots cet article: {text}?",
            ["count", "text"],
            "alias2",
        ),
    ],
)
def test_prompt_template_schema(template, variables, alias):
    """Assert prompt template parsing."""
    template = PromptTemplateSchema(template=template, alias=alias)

    assert variables == template.variables


@pytest.mark.parametrize(
    "template, values, alias, expected_prompt",
    (
        (
            "What are the main topics discussed in this text: {text}",
            {
                "text": "Apple today announced its manufacturing partners now support over 13 gigawatts of renewable electricity around the world, a nearly 30 percent increase in the last year. In total, more than 250 suppliers operating across 28 countries are committed to using renewable energy for all Apple production by 2030"  # noqa: E501
            },
            "alias1",
            "What are the main topics discussed in this text: Apple today announced its manufacturing partners now support over 13 gigawatts of renewable electricity around the world, a nearly 30 percent increase in the last year. In total, more than 250 suppliers operating across 28 countries are committed to using renewable energy for all Apple production by 2030",  # noqa: E501
        ),
        (
            "What's the most popular {type} framework?",
            {"type": "machine-learning"},
            "alias2",
            "What's the most popular machine-learning framework?",
        ),
        (
            "Peux-tu resumer en moins de {count} mots cet article: {text}?",
            {
                "count": "20",
                "text": "L'inflation annuelle est l'évolution des prix des biens de consommation et des services entre le mois de référence et le même mois de l'année précédente.",  # noqa: E501
            },
            "alias3",
            "Peux-tu resumer en moins de 20 mots cet article: L'inflation annuelle est l'évolution des prix des biens de consommation et des services entre le mois de référence et le même mois de l'année précédente.?",  # noqa: E501
        ),
    ),
)
def test_generate_prompt(template, values, alias, expected_prompt):
    """Assert prompt generation from template."""
    template = PromptTemplateSchema(template=template, alias=alias)
    assert template.prompt(**values) == expected_prompt


@pytest.mark.parametrize(
    "template, alias",
    [
        ("What are the main topics discussed in this text: {text}.", "alias1"),
        ("Peux-tu resumer en {count} mots cet article: {text}?", "alias2"),
    ],
)
@patch("src.db.Model.save")
def test_save_prompt_template_schema(mock_save, template, alias):
    """Assert prompt initialization"""
    template = PromptTemplateSchema(template=template, alias=alias)

    saved_template = template.save()

    mock_save.assert_called_once()

    assert isinstance(saved_template.id, str)
    assert isinstance(saved_template.created_at, str)
    assert isinstance(saved_template.template, str)
    assert isinstance(saved_template.alias, str)


@pytest.mark.parametrize(
    "id",
    ["39ba8bf2-3a40-42a2-9ca1-27fa3de39e2b", "69095223-dae8-47ad-a077-150e5c5986db"],
)
@patch.object(PromptTemplateTable, "get")
def test_get_template_schema_with_id(mock_get, id):
    """Test retrieve template with id."""
    mock_get.return_value = PromptTemplateTable(
        id=id,
        template="template",
        alias="alias",
        created_at=datetime.now(timezone.utc),
    )
    _ = PromptTemplateSchema.get(id)
    mock_get.assert_called_with(id)


@patch.object(PromptTemplateTable, "scan")
def test_get_template_schema_without_id(mock_scan):
    """Test retrieve all templates."""
    # TODO: add a test case that return values.
    mock_scan.return_value = []
    assert PromptTemplateSchema.get() == []
    mock_scan.assert_called_once()


@pytest.mark.parametrize(
    "id",
    ["39ba8bf2-3a40-42a2-9ca1-27fa3de39e2b", "69095223-dae8-47ad-a077-150e5c5986db"],
)
@patch("src.prompt.tables.PromptTemplateTable.update")
@patch.object(PromptTemplateTable, "get")
def test_update_template_schema(mock_get, mock_prompt_update, id):
    """Test update template schema."""
    prompt = PromptTemplateSchema(id=id, template="template", alias="alias")
    mock_get.return_value = PromptTemplateTable(
        id=id,
        template="template",
        alias="alias",
        created_at=datetime.now(timezone.utc),
    )

    prompt.update()

    mock_get.assert_called_with(id)
    mock_prompt_update.assert_called_once()
