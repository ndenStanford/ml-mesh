"""Initialization of the MultiEL model."""

# Standard Library
import logging
import os
from typing import Any, Dict, List

# Source
from .bela_model import BelaModel


logger = logging.getLogger(__name__)


class BELA:
    """Bela model initialization."""

    def __init__(
        self,
        md_threshold: float = 0.2,
        el_threshold: float = 0.4,
        checkpoint_name: str = "wiki",
        device: str = "cuda:0",
        config_name: str = "joint_el_mel_new",
        repo: str = "wannaphong/BELA",
    ):
        """Initializes the model through 'conf' subfolder."""
        self.md_threshold = md_threshold
        self.el_threshold = el_threshold
        self.config_name = config_name
        self.device = device
        self.repo = repo
        self.checkpoint_name_path = f"model_{checkpoint_name}.ckpt"
        if checkpoint_name not in ["aida", "e2e", "mewsli", "wiki"]:
            logger.warning(
                f"Your checkpoint name is not in the list, so we will load {checkpoint_name} as path in {repo}"  # noqa
            )
            self.checkpoint_name_path = checkpoint_name
        self.ent_catalogue_idx_path = os.path.join(self.repo, "index.txt")
        self.checkpoint_path = os.path.join(self.repo, self.checkpoint_name_path)
        self._load_model()

    def _load_model(self) -> None:
        """Load model."""
        self.model = BelaModel(
            self.checkpoint_path,
            config_name=self.config_name,
            ent_catalogue_idx_path=self.ent_catalogue_idx_path,
            device=self.device,
        )
        self.model.task.md_threshold = self.md_threshold
        self.model.task.el_threshold = self.el_threshold

    def process_batch(self, list_text: list) -> List[Dict[str, Any]]:
        """Call for batch processing."""
        return self.model.process_batch(list_text)

    def process_disambiguation_batch(
        self,
        list_text: list,
        mention_offsets: list,
        mention_lengths: list,
        entities: list,
    ) -> List[Dict[str, Any]]:
        """Call for batch disambiguation processing."""
        return self.model.process_disambiguation_batch(
            texts=list_text,
            mention_offsets=mention_offsets,
            mention_lengths=mention_lengths,
            entities=entities,
        )
