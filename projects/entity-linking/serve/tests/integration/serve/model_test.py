"""Model test."""

# 3rd party libraries
import pytest


@pytest.mark.parametrize(
    "query, valid_expected_responses",
    [
        (
            {
                "text": "Hello, nothing to see here. Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium. Arsenal is not so bad either.",  # noqa
                "entities": [
                    {
                        "entity_type": "ORG",
                        "entity_text": "Tottenham Hotspur Football Club",
                        "score": 0.9259419441223145,
                        "sentence_index": 1,
                    },
                    {
                        "entity_type": "ORG",
                        "entity_text": "Arsenal",
                        "score": 0.9259419441223145,
                        "sentence_index": 2,
                    },
                ],
            },
            [
                (
                    ["Tottenham Hotspur Football Club", "Arsenal"],
                    [0, 0],
                    [28, 150],
                    [31, 7],
                ),
                (
                    ["Arsenal", "Tottenham Hotspur Football Club"],
                    [0, 0],
                    [150, 28],
                    [7, 31],
                ),
            ],
        )
    ],
)
def test__generate_offsets(entity_linking_model, query, valid_expected_responses):
    """Test query wiki."""
    text = query["text"]
    entities = query["entities"]
    result = entity_linking_model._generate_offsets(text, entities)

    assert (
        result in valid_expected_responses
    ), f"Result {result} not in expected responses {valid_expected_responses}"
