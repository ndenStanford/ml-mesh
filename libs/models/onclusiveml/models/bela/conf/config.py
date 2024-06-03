"""Configuration BELA model script."""

# Standard Library
from functools import lru_cache
from typing import Any, Optional

# 3rd party libraries
from pydantic import BaseModel, Field

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings


class TransformSettings(OnclusiveBaseSettings):
    _target_ = "onclusiveml.models.bela.transforms.joint_el_transform.JointELXlmrRawTextTransform"
    max_seq_len: int = 256


class DataModuleSettings(OnclusiveBaseSettings):
    _target_: str = (
        "onclusiveml.models.bela.datamodule.joint_el_datamodule.JointELDataModule"
    )
    batch_size: int = 24
    drop_last: bool = True
    train_path: Optional[str] = "/fsx/movb/data/matcha/mel/train.1st.txt"
    val_path: Optional[str] = "/fsx/movb/data/matcha/mel/eval.1st.txt"
    test_path: Optional[str] = "/fsx/movb/data/matcha/mel/test.1st.txt"
    ent_catalogue_idx_path: str = "/fsx/movb/data/matcha/mel/index_new.txt"
    transform: TransformSettings = TransformSettings()


class OptimSettings(OnclusiveBaseSettings):
    _target_: str = "torch.optim.AdamW"
    lr: float = 1e-05
    betas: list = [0.9, 0.999]
    eps: float = 1e-08
    weight_decay: float = 0
    amsgrad: bool = False


class ModelSettings(OnclusiveBaseSettings):
    _target_: str = "onclusiveml.models.bela.models.hf_encoder.HFEncoder"
    model_path: str = "xlm-roberta-large"


class TrainerSettings(OnclusiveBaseSettings):
    gpus: int = 8
    num_nodes: int = 1
    max_epochs: int = 3
    num_sanity_val_steps: int = 0
    log_every_n_steps: int = 10
    gradient_clip_val: float = 2.0
    accumulate_grad_batches: int = 1
    accelerator: str = "gpu"
    strategy: str = "ddp_sharded"
    precision: int = 16
    default_root_dir: str = "/checkpoints/${oc.env:USER}/bela/${now:%Y-%m-%d-%H%M%S}"
    val_check_interval: int = 3000
    limit_val_batches: int = 500

    class Config:
        extra = "allow"


class CheckpointCallbackSettings(OnclusiveBaseSettings):
    _target_: str = "pytorch_lightning.callbacks.ModelCheckpoint"
    monitor: str = "valid_f1"
    mode: str = "max"
    save_last: bool = True
    verbose: bool = True
    filename: str = "checkpoint_best"
    save_top_k: int = -1
    save_weights_only: bool = True


class TaskSettings(OnclusiveBaseSettings):
    _target_: str = Field(
        default="onclusiveml.models.bela.task.joint_el_task.JointELTask"
    )
    only_train_disambiguation: bool = Field(default=False)
    train_saliency: bool = Field(default=False)
    embeddings_path: str = Field(default="/fsx/movb/data/matcha/mel/embeddings_new.pt")
    use_gpu_index: bool = Field(default=True)
    load_from_checkpoint: str = Field(
        default="/checkpoints/movb/bela/2023-01-13-023711/0/lightning_logs/version_4144/checkpoints/last.ckpt"
    )

    optim: OptimSettings = OptimSettings()
    transform: TransformSettings = TransformSettings()
    model: ModelSettings = ModelSettings()
    datamodule: Optional[Any] = None
    trainer: TrainerSettings = TrainerSettings()
    checkpoint_callback: CheckpointCallbackSettings = CheckpointCallbackSettings()
    _recursive_: Optional[bool] = False


class GlobalSettings(
    OnclusiveBaseSettings,
):
    """Global server settings."""

    task: Optional[TaskSettings] = TaskSettings()
    datamodule: Optional[DataModuleSettings] = DataModuleSettings()
    trainer: Optional[TrainerSettings] = TrainerSettings()

    class Config:
        extra = "allow"


@lru_cache
def get_settings() -> GlobalSettings:
    """Returns instantiated global settings class."""
    return GlobalSettings()
