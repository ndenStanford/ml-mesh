# Standard Library
import shutil
from datetime import datetime as dt
from typing import Union

# ML libs
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from transformers.pipelines import Pipeline, pipeline


def duplicate_huggingface_transformer_via_local_cache(
    huggingface_transformer: Union[
        PreTrainedTokenizer, PreTrainedTokenizerFast, Pipeline
    ]
) -> Union[PreTrainedTokenizer, PreTrainedTokenizerFast, Pipeline]:
    """Saves and re-imports the passed tokenizer or pipeline instance to effectively
    create a deep copy."""
    # export and re-import tokenizer to avoid changing in place
    local_temp_dir = f'temp_{dt.now().strftime("%Y_%m_%d__%H_%M_%s")}'
    huggingface_transformer.save_pretrained(local_temp_dir)

    if isinstance(
        huggingface_transformer, (PreTrainedTokenizer, PreTrainedTokenizerFast)
    ):
        duplicated_transformer = huggingface_transformer.from_pretrained(local_temp_dir)
    elif isinstance(huggingface_transformer, Pipeline):
        duplicated_transformer = pipeline(
            task=huggingface_transformer.task, model=local_temp_dir
        )
    else:
        try:
            duplicated_transformer = huggingface_transformer.from_pretrained(local_temp_dir)
        except NotImplementedError as e:
            raise e

    shutil.rmtree(local_temp_dir)

    return duplicated_transformer
