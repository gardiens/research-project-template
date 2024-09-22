from typing import TYPE_CHECKING, Optional, Tuple

import hydra
import torch
import torch.optim as optim
from clearml import Task
from omegaconf import DictConfig, OmegaConf

from src.logger.clearml import connect_whole
from src.loss import CrossEntropyLoss
from src.transforms.naive_transforms import transform_train

# Registering the "eval" resolver allows for advanced config
# interpolation with arithmetic operations:
# https://omegaconf.readthedocs.io/en/2.3_branch/how_to_guides.html
OmegaConf.register_new_resolver("eval", eval)
import random

import numpy as np

if TYPE_CHECKING:
    from src.dataset.cifar import BaseDataModule
    from src.trainer import Trainer


def set_seed(seed) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.cuda.manual_seed_all(seed)


def train(cfg: DictConfig, task: Task) -> None:
    """Trains the model. Can additionally evaluate on a testset, using best weights obtained during
    training.

    This method is wrapped in optional @task_wrapper decorator which applies extra utilities
    before and after the call.

    Args:
        cfg (DictConfig): Configuration composed by Hydra.

    Returns:
        Tuple[dict, dict]: Dict with metrics and dict with all instantiated objects.
    """
    instantiator = hydra.utils.instantiate
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_built()
        else "cpu"
    )
    set_seed(cfg.seed)
    base_datamodule: "BaseDataModule" = hydra.utils.instantiate(cfg.dataset)
    train_loader, val_loader, test_loader = base_datamodule.get_dataset(transform_train)
    criterion = instantiator(
        cfg.loss
    )  # should be either the CrossEntropyLoss; or the HierarchicalLoss or HierarchicalLossConvex

    net = instantiator(cfg.model).to(device)

    optimizer = optim.Adam(net.parameters(), lr=cfg.trainer.learning_rate)
    if cfg.get("clearml"):
        clearml_setup = True
        connect_whole(
            cfg=cfg,
            task=task,
            name_connect_cfg="whole train cfg",
            name_hyperparams_summary="summary train cfg",
        )
        logger_clearml = task.get_logger()
    else:
        clearml_setup = False

    logger = instantiator(config=cfg.logger)
    trainer: "Trainer" = instantiator(
        cfg.trainer,
        train_loader=train_loader,
        val_loader=val_loader,
        test_loader=test_loader,
        net=net,
        logger=logger,
        device=device,
    )
    #! actual training step
    trainer.train(optimizer, criterion)


@hydra.main(version_base="1.2", config_path="configs", config_name="train.yaml")
def main(cfg: DictConfig) -> None:
    # fetch cleamrl, must be at the beginning or the logging will not be perfect

    if cfg.get("clearml"):
        task: Task = hydra.utils.instantiate(cfg.clearml)
    else:
        task = None
    # actual computation
    return train(cfg, task=task)


if __name__ == "__main__":
    main()
