# ML libs
from keybert.backend._hftransformers import HFTransformerBackend

# Internal libraries
from onclusiveml.ml_compile import CompiledPipeline


class CompiledHFTransformerBackend(HFTransformerBackend):
    def __init__(self, embedding_model: CompiledPipeline):

        if isinstance(embedding_model, CompiledPipeline):
            self.embedding_model = embedding_model
        else:
            raise ValueError(
                "Please select a correct compiled transformers pipeline. For example: "
                "CompiledPipeline.from_pipeline("
                "   pipeline("
                "       'feature-extraction',"
                "       model='distilbert-base-cased',"
                "       device=0"
                "   )"
                ")"
            )
