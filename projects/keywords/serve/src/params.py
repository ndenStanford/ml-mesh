"""Settings."""

# Standard Library
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving import ServingBaseParams


class ServedModelParams(ServingBaseParams):
    """Prediction model parameters."""

    model_name: str = "keywords"
    model_directory: Union[str, Path] = "."
