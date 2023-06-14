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
    assert isinstance(saved_template.created_at, datetime)
    assert isinstance(saved_template.template, str)
    assert isinstance(saved_template.alias, str)


@pytest.mark.parametrize(
    "alias",
    ["alias-1", "alias-2"],
)
@patch.object(PromptTemplateTable, "query")
def test_get_template_schema_with_alias(mock_query, alias):
    """Test retrieve template with alias."""
    mock_query.return_value = [
        PromptTemplateTable(
            id=1,
            template="template",
            alias="alias",
            created_at=datetime.now(timezone.utc),
        )
    ]
    _ = PromptTemplateSchema.get(alias)
    mock_query.assert_called_with(alias, scan_index_forward=False)


@pytest.mark.parametrize(
    "alias, version",
    [("alias-1", 1), ("alias-2", 2)],
)
@patch.object(PromptTemplateTable, "query")
def test_get_template_schema_with_alias_and_version(mock_query, alias, version):
    """Test retrieve template with alias."""
    mock_query.return_value = [
        PromptTemplateTable(
            id=1,
            template="template",
            alias="alias",
            version=version,
            created_at=datetime.now(timezone.utc),
        )
    ]
    _ = PromptTemplateSchema.get(alias, version=version)
    mock_query.assert_called_once()


@patch.object(PromptTemplateTable, "scan")
def test_get_template_schema_without_id(mock_scan):
    """Test retrieve all templates."""
    # TODO: add a test case that return values.
    mock_scan.return_value = []
    assert PromptTemplateSchema.get() == []
    mock_scan.assert_called_once()


@pytest.mark.parametrize(
    "id, alias, template, updated_template",
    [
        (
            "ac6b630d-ad44-4f7a-b306-402fdd62ecdd",
            "joke",
            "Tell me a joke",
            "Tell me a joke about {topic}",
        ),
        (
            "30b5b324-5f1b-486e-8771-6946b9762183",
            "write-an-essay",
            "Write a {count}-word essay about {topic}",
            "Write an essay about {topic} in less than {count} words.",
        ),
    ],
)
@patch.object(PromptTemplateSchema, "save")
@patch.object(PromptTemplateTable, "query")
def test_update_template_schema(
    mock_query, mock_prompt_save, id, alias, template, updated_template
):
    """Test update template schema."""
    prompt = PromptTemplateSchema(id=id, template=template, alias=alias)

    mock_query.return_value = [
        PromptTemplateTable(
            id=id,
            template=template,
            alias=alias,
            created_at=datetime.now(timezone.utc),
        )
    ]

    prompt.update(template=updated_template)

    mock_query.assert_called_with(alias, scan_index_forward=False)
    mock_prompt_save.assert_called_once()
