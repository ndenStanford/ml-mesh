# Standard Library
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving import ServingBaseParams


class ServedModelParams(ServingBaseParams):

    model_name: str = "ner"
    model_directory: Union[str, Path] = "."
