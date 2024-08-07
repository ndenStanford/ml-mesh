"""Encoder."""

# Standard Library
from typing import Optional

# ML libs
import torch.nn as nn
from transformers import AutoModel

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=20)


class HFEncoder(nn.Module):
    """Encoder."""

    def __init__(
        self,
        model_path: str = "xlm-roberta-base",
        projection_dim: Optional[int] = None,
    ):
        super().__init__()
        self.transformer = AutoModel.from_pretrained(
            model_path, device_map="auto", torch_dtype="auto"
        )
        self.embedding_dim = self.transformer.encoder.config.hidden_size
        self.max_length = 256

    def forward(self, input_ids, attention_mask=None):
        """Forward Encoder."""
        output = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        last_layer = output["last_hidden_state"]
        sentence_rep = last_layer[:, 0, :]
        return sentence_rep, last_layer
