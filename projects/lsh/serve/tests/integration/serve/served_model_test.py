# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedLshModel
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(1)
def test_served_lsh_model__init__():
    """Tests the constructor of the ServedLshModel, EXCLUDING the loading of genuine model
    artifacts from local disk"""

    ServedLshModel()


@pytest.mark.order(2)
def test_served_lsh_model_load():
    """Tests the constructor of the ServedLSHModel, INCLUDING the loading of genuine model
    artifacts from local disk"""

    served_lsh_model = ServedLshModel()

    assert not served_lsh_model.is_ready()

    served_lsh_model.load()

    assert served_lsh_model.is_ready()


@pytest.mark.order(3)
@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_lsh_model_predict(
    test_inputs,
    test_predictions,
    test_record_index,
):
    """Tests the fully initialized and loaded ServedLshModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_lsh_model = ServedLshModel()
    served_lsh_model.load()

    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=[
            PredictInputDocumentModel(
                content="Call functions to generate hash signatures for each article",
                language="en",
            )
        ],
    )

    actual_output = served_lsh_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=[
            "AAAAAD7VrJYAAAAAUtj2YwAAAABnUo5LAAAAAKEQ6osAAAAAGN7zAQAAAACvI05uAAAAAP5T14M=",
            "AAAAAImeBE8AAAAArLzBiwAAAABXJtUuAAAAADuLk0EAAAAABdQyawAAAABsuvhdAAAAAA1DABQ=",
            "AAAAAN80jQ0AAAAA4AMsTwAAAAAdQ+nJAAAAADQX7AwAAAAAOInWSgAAAADW8ezsAAAAALmkSmc=",
            "AAAAAEdhYYkAAAAAdlWvggAAAABKailoAAAAAAIxAgoAAAAATpd/swAAAABwtMk4AAAAABkBF2c=",
            "AAAAAMTyc2oAAAAARNwyWAAAAABz/P6bAAAAACTaVUQAAAAAMoyr9gAAAACESd6KAAAAAFgDYYc=",
            "AAAAAFKn1w8AAAAA3LGTrAAAAAAJJ73aAAAAAAtnQgYAAAAAc4I7eAAAAAD08z7vAAAAAEWmb0M=",
            "AAAAANYBf2oAAAAAU59svQAAAABWfyecAAAAAO+fMSoAAAAA/AEiWQAAAADi76dRAAAAACZAFWI=",
            "AAAAAKceSGYAAAAAHHnbRwAAAACNhF50AAAAAHgsIHIAAAAALQe0tgAAAACl0hKtAAAAANjd5Gw=",
            "AAAAAJFzk3gAAAAAMxIZewAAAABmmIwNAAAAANKJgxMAAAAAaeBdxQAAAAByhAtTAAAAAKoPEtA=",
            "AAAAAD//H6QAAAAAR2MGtQAAAADuHvbsAAAAANOxgcsAAAAAbMURIgAAAABUGFjvAAAAAA2+Lew=",
            "AAAAADJ0nxwAAAAAEDygXwAAAAC5rKeMAAAAAMHGBJAAAAAAVbu+HAAAAACvnHsdAAAAAPZ4r3I=",
            "AAAAAIsaapQAAAAA4UNh0wAAAAD29SlWAAAAAKgaBv4AAAAABK518AAAAACE0OvYAAAAAPYUu7c=",
            "AAAAAPgAVJoAAAAAR8Y3RQAAAAD1tPyTAAAAAPeLD0EAAAAAnAxBywAAAABKiF6rAAAAAGoBEXA=",
            "AAAAAGQyfFMAAAAAGFRsIAAAAAAiQRcGAAAAADzs6CYAAAAABT6eXgAAAADBDsR/AAAAAKjSFEc=",
            "AAAAAMsg8FIAAAAAFm7yPAAAAAA5Au8cAAAAAGYhiuUAAAAA9jbZdQAAAAB2X3QvAAAAAO+93YE=",
            "AAAAAOrGfusAAAAA4UQsGgAAAAB9n0NhAAAAAFDZRUIAAAAAbKUEUQAAAABSgqcrAAAAANReZwE=",
            "AAAAANrB0GcAAAAAkNMRaAAAAAA0QhyKAAAAABLE06gAAAAAzi1LqAAAAACo+jipAAAAAIUoHM4=",
            "AAAAAHxFrisAAAAAkf5FlgAAAACQ7ru+AAAAAO4TeqUAAAAAcsOYLwAAAAAHk+gFAAAAAHSHwzQ=",
        ]
    )

    assert actual_output == expected_output


@pytest.mark.order(3)
def test_served_lsh_model_bio(test_model_name, test_model_card):
    """Tests the fully initialized and loaded ServedLshModel's bio method, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    served_lsh_model = ServedLshModel()

    served_lsh_model.load()

    actual_output = served_lsh_model.bio()
    expected_output = BioResponseModel(model_name="lsh")

    assert actual_output == expected_output
