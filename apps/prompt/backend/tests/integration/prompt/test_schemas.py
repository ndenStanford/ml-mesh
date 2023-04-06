"""Test schemas."""

# 3rd party libraries
import pytest

# Source
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


@pytest.mark.parametrize(
    "template",
    [
        "Quiero un breve resumen de dos líneas de este texto: {text}",
        "Quel est le framework {type} le plus populaire?",
    ],
)
def test_save(template):
    """Test save schema in db."""
    schema = PromptTemplateSchema(template=template)

    saved_schema = schema.save()

    assert saved_schema.id is not None
    assert saved_schema.created_at is not None
    assert PromptTemplateTable.count() > 0


@pytest.mark.parametrize(
    "template",
    [
        "Translate this text {text} from {source_lang} to {target_lang}",
        "Ecris une dissertation de {count} mots sur le sujet suivant {topic}",
    ],
)
def test_get_exists(template):
    """Test get item from table."""
    schema = PromptTemplateSchema(template=template).save()

    schema_from_db = PromptTemplateSchema.get(schema.id)

    assert schema.id == schema_from_db.id
    assert schema.created_at == schema_from_db.created_at
    assert schema.template == schema_from_db.template


@pytest.mark.parametrize(
    "template, updated_template",
    [
        (
            "Transalte this test {text} to {target_lang}",
            "Translate this text {text} from {source_lang} to {target_lang}",
        )
    ],
)
def test_update(template, updated_template):
    """Test get item from table."""
    schema = PromptTemplateSchema(template=template).save()

    schema.update(template=updated_template)

    updated_schema = PromptTemplateSchema.get(schema.id)

    assert updated_schema.id == schema.id
    assert updated_schema.created_at == schema.created_at
    assert updated_schema.template == updated_template
    assert updated_schema.template != schema.template
