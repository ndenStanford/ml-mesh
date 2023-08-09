# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedLshModel
from src.serve.server_models import (
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictRequestModel,
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
def test_served_lsh_model_predict(test_predict_input, test_expected_predict_output):
    """Tests the fully initialized and loaded ServedLshModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_lsh_model = ServedLshModel()
    served_lsh_model.load()

    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=PredictInputDocumentModel(
            content=test_predict_input,
        ),
    )

    test_actual_predict_output = served_lsh_model.predict(input)

    assert test_actual_predict_output == test_expected_predict_output


@pytest.mark.order(3)
def test_served_lsh_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedLshModel's bio method, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    served_lsh_model = ServedLshModel()

    served_lsh_model.load()

    test_actual_bio_output = served_lsh_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
