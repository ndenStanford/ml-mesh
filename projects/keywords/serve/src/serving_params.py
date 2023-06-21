# Standard Library
import os
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving.rest.serve import ServingBaseParams


class ServedModelParams(ServingBaseParams):

    model_name: str = "keywords_model"

    model_artifact_directory: Union[str, Path] = os.path.join(
        "src", "keywords_model_artifacts"
    )

    model_card_file: Union[str, Path] = os.path.join(
        "src", "keywords_model_artifacts", "model_card.json"
    )

    inputs_test_file: Union[str, Path] = os.path.join(
        "src", "keywords_model_artifacts", "inputs.json"
    )
    inference_params_test_file: Union[str, Path] = os.path.join(
        "src", "keywords_model_artifacts", "inference_params.json"
    )
    predictions_test_file: Union[str, Path] = os.path.join(
        "src", "keywords_model_artifacts", "predictions.json"
    )
