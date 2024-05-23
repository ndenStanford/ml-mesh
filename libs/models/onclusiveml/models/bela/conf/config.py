# Standard Library
from dataclasses import dataclass, field
from typing import Any, List


# @manual "//github/facebookresearch/hydra:hydra"
# from hydra.core.config_store import ConfigStore
# from omegaconf import MISSING


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
