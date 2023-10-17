"""Settings."""

# Standard Library
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving import ServingBaseParams


class ServedModelParams(ServingBaseParams):
    """Prediction model settings."""

    model_name: str = "iptc"
    model_directory: Union[str, Path] = "."
