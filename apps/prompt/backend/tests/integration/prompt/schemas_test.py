"""Schemas Test."""

# 3rd party libraries
import pytest
from freezegun import freeze_time

# Source
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


@pytest.mark.parametrize(
    "template, alias",
    [
        (
            "Quiero un breve resumen de dos líneas de este texto: {text}",
            "alias1",
        ),
        (
            "Quel est le framework {type} le plus populaire?",
            "alias2",
        ),
    ],
)
def test_save(template, alias):
    """Test save schema in db."""
    schema = PromptTemplateSchema(template=template, alias=alias)

    saved_schema = schema.save()

    assert saved_schema.id is not None
    assert saved_schema.created_at is not None
    assert PromptTemplateTable.count() > 0


@pytest.mark.parametrize(
    "template, alias",
    [
        (
            "Translate this text {text} from {source_lang} to {target_lang}",
            "alias3",
        ),
        (
            "Ecris une dissertation de {count} mots sur le sujet suivant {topic}",
            "alias4",
        ),
    ],
)
def test_get_exists(template, alias):
    """Test get item from table."""
    schema = PromptTemplateSchema(template=template, alias=alias).save()

    schema_from_db = PromptTemplateSchema.get(schema.alias)[0]

    assert schema.id == schema_from_db.id
    assert schema.created_at == schema_from_db.created_at
    assert schema.template == schema_from_db.template
    assert schema.alias == schema_from_db.alias


@pytest.mark.parametrize(
    "template, alias, updated_template",
    [
        (
            "Transalte this test {text} to {target_lang}",
            "alias-5",
            "Translate this text {text} from {source_lang} to {target_lang}",
        )
    ],
)
@freeze_time("2012-01-14 03:21:34")
def test_update(template, alias, updated_template):
    """Test get item from table."""
    schema = PromptTemplateSchema(template=template, alias=alias).save()

    schema.update(template=updated_template)

    updated_schema = PromptTemplateSchema.get(schema.alias)[0]

    assert updated_schema.id != schema.id  # new version created
    assert updated_schema.created_at == schema.created_at
    assert updated_schema.template == updated_template
    assert updated_schema.alias == alias
    assert updated_schema.template != schema.template
