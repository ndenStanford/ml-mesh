# Standard Library
from pathlib import Path

# 3rd party libraries
import yaml

# Source
from .pydantic_config import MainConfig


config_data = {
    "task": {
        "_target_": "onclusiveml.models.bela.task.joint_el_task.JointELTask",
        "datamodule": None,
        "transform": {
            "_target_": "onclusiveml.models.bela.transforms.joint_el_transform.JointELXlmrRawTextTransform",
            "max_seq_len": 256,
        },
        "model": {
            "_target_": "onclusiveml.models.bela.models.hf_encoder.HFEncoder",
            "model_path": "xlm-roberta-large",
        },
        "optim": {
            "_target_": "torch.optim.AdamW",
            "lr": 1e-05,
            "betas": [0.9, 0.999],
            "eps": 1e-08,
            "weight_decay": 0,
            "amsgrad": False,
        },
        "only_train_disambiguation": False,
        "train_saliency": False,
        "embeddings_path": "/fsx/movb/data/matcha/mel/embeddings_new.pt",
        "use_gpu_index": True,
        "load_from_checkpoint": "/checkpoints/movb/bela/2023-01-13-023711/0/lightning_logs/version_4144/checkpoints/last.ckpt",
    },
    "datamodule": {
        "_target_": "onclusiveml.models.bela.datamodule.joint_el_datamodule.JointELDataModule",
        "batch_size": 24,
        "drop_last": True,
        "train_path": "/fsx/movb/data/matcha/mel/train.1st.txt",
        "val_path": "/fsx/movb/data/matcha/mel/eval.1st.txt",
        "test_path": "/fsx/movb/data/matcha/mel/test.1st.txt",
        "ent_catalogue_idx_path": "/fsx/movb/data/matcha/mel/index_new.txt",
    },
    "trainer": {
        "gpus": 8,
        "num_nodes": 1,
        "max_epochs": 3,
        "num_sanity_val_steps": 0,
        "log_every_n_steps": 10,
        "gradient_clip_val": 2.0,
        "accumulate_grad_batches": 1,
        "accelerator": "gpu",
        "strategy": "ddp_sharded",
        "precision": 16,
        "default_root_dir": "/checkpoints/${oc.env:USER}/bela/${now:%Y-%m-%d-%H%M%S}",
        "val_check_interval": 3000,
        "limit_val_batches": 500,
    },
    "test_only": False,
    "checkpoint_callback": {
        "_target_": "pytorch_lightning.callbacks.ModelCheckpoint",
        "monitor": "valid_f1",
        "mode": "max",
        "save_last": True,
        "verbose": True,
        "filename": "checkpoint_best",
        "save_top_k": -1,
        "save_weights_only": True,
    },
}

config = MainConfig(**config_data)
