# Standard Library
from copy import deepcopy
from typing import Union

# ML libs
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from transformers.pipelines import Pipeline


def duplicate_huggingface_transformer_via_local_cache(
    huggingface_transformer: Union[
        PreTrainedTokenizer, PreTrainedTokenizerFast, Pipeline
    ]
) -> Union[PreTrainedTokenizer, PreTrainedTokenizerFast, Pipeline]:
    return deepcopy(huggingface_transformer)
