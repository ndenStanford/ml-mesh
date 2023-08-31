"""Backend transformer."""

# ML libs
from keybert.backend._hftransformers import HFTransformerBackend
from transformers.pipelines import Pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline


class CustomHFTransformerBackend(HFTransformerBackend):
    """Custom Transformer backend."""

    def __init__(self, embedding_model: CompiledPipeline):
        if isinstance(embedding_model, (CompiledPipeline, Pipeline)):
            self.embedding_model = embedding_model
        else:
            raise ValueError(
                "Please select either a CompiledPipeline or Pipeline instance."
            )
