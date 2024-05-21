# Standard Library
from dataclasses import dataclass, field
from typing import Any, List

# 3rd party libraries
# @manual "//github/facebookresearch/hydra:hydra"
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING


defaults = [
    "_self_",
    {"task": "joint_el_task"},
    # Model
    # {"task/model": "xlmr"},
    # Transform
    # {"task/transform": "joint_el_xlmr_transform"},
    # Optim
    # {"task/optim": "adamw"},
    # Data
    # {"datamodule": "joint_el_datamodule"},
    # Trainer
    # {"trainer": "gpu_1_host"},
    {"checkpoint_callback": "default"},
]


@dataclass
class MainConfig:
    defaults: List[Any] = field(default_factory=lambda: defaults)
    task: Any = MISSING
    datamodule: Any = MISSING
    trainer: Any = MISSING
    test_only: bool = False
    checkpoint_callback: Any = MISSING


cs = ConfigStore.instance()

cs.store(name="config", node=MainConfig)
