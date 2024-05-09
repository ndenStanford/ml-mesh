from .bela_model import BelaModel
import os
import logging

logger = logging.getLogger(__name__)


class BELA:
    def __init__(self, md_threshold:float=0.2, el_threshold:float=0.4, checkpoint_name: str="wiki", device: str="cuda:0", config_name:str="joint_el_mel_new", repo:str="wannaphong/BELA"):
        self.md_threshold = md_threshold
        self.el_threshold = el_threshold
        self.config_name = config_name
        self.device = device
        self.repo=repo
        self.checkpoint_name_path = f"model_{checkpoint_name}.ckpt"
        if checkpoint_name not in ["aida", "e2e", "mewsli", "wiki"]:
            logger.warning(f"Your checkpoint name is not in the list, so we will load {checkpoint_name} as path in {repo}")
            self.checkpoint_name_path = checkpoint_name
        self.embeddings_path=os.path.join(self.repo, "embeddings.pt")
        self.ent_catalogue_idx_path=os.path.join(self.repo, "index.txt")
        self.checkpoint_path=os.path.join(self.repo, self.checkpoint_name_path)
        print("embeddings_path: ", self.embeddings_path)
        print("ent_catalogue: ", self.ent_catalogue_idx_path)
        print("checkpoint_path: ", self.checkpoint_path)
        self._load_model()
    def _load_model(self):
        self.model = BelaModel(self.checkpoint_path,config_name=self.config_name,embeddings_path=self.embeddings_path,ent_catalogue_idx_path=self.ent_catalogue_idx_path,device=self.device)
        self.model.task.md_threshold = self.md_threshold
        self.model.task.el_threshold = self.el_threshold
    def process_batch(self, list_text:list):
        return self.model.process_batch(list_text)
