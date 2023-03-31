from transformers.pipelines import Pipeline
from torch.jit._trace import TopLevelTracedModule
from torch.jit._script import RecursiveScriptModule
from transformers.utils.generic import ModelOutput
from typing import Union, Dict


def compile_pipeline(
    pipeline: Pipeline,
    traced_model: Union[TopLevelTracedModule, RecursiveScriptModule], # traced output model type and save->load reimported model type
    tokenizer_settings: Dict,
) -> Pipeline:
    """Utility function to take a conventional huggingface transformers pipeline and replace
    its model component with a (neuron)-torchscript model.

    This includes fixing the tokenizer to always use the same tokenization behaviour to
    ensure consistent sequence lengths, and optional postprocessing of the model outputs
    to avoid key errors based on dict types not supporting integer indexig.

    NOTE: The passed argument 'pipeline' will be returned but ALSO modified in place."""

    # attach additional tokenizer setting attribute to pipeline
    pipeline.tokenizer_settings = tokenizer_settings

    original_tokenizer = pipeline.tokenizer

    # --- update pipeline's tokenizer logic with fixed logic
    def fixed_tokenizer(*args, **kwargs):
        kwargs["padding"] = tokenizer_settings["padding"]
        kwargs["add_special_tokens"] = tokenizer_settings["add_special_tokens"]
        # this is the key line here to set a static input shape
        # so that all inputs are set to a len of 128
        kwargs["max_length"] = tokenizer_settings["max_length"]
        kwargs["truncation"] = tokenizer_settings["truncation"]
        
        return original_tokenizer(*args, **kwargs)

    pipeline.tokenizer = fixed_tokenizer
    pipeline.tokenizer.decode = original_tokenizer.decode
    pipeline.tokenizer.mask_token_id = original_tokenizer.mask_token_id
    pipeline.tokenizer.pad_token_id = original_tokenizer.pad_token_id
    pipeline.tokenizer.convert_ids_to_tokens = original_tokenizer.convert_ids_to_tokens

    # --- update pipeline's model logic with additional postprocessing required for
    # some pipeline types (e.g. feature-extraction)
    def adaptive_model(*args, **kwargs):
        
        # assemble model inputs depending on the kwargs keys
        model_input = [kwargs['input_ids']]
        
        if 'attention_mask' in kwargs.keys():
            model_input.append(kwargs['attention_mask'])
        
        if 'token_type_ids' in kwargs.keys():
            model_input.append(kwargs['token_type_ids'])
            
        predictions = traced_model(*model_input)

        if isinstance(predictions, dict):
            formatted_predictions = ModelOutput(predictions)
        else:
            formatted_predictions = predictions

        return formatted_predictions

    original_model_config = pipeline.model.config

    pipeline.model = adaptive_model
    pipeline.model.config = original_model_config

    return pipeline