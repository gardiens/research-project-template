# content of test_sample.py
# add the parent subfolder to path
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from train import *  # noqa: F403


def test_import():
    # import were done before if needs be
    assert 4 == 4


def test_model():
    pass 


from omegaconf import DictConfig, open_dict


def test_instantiate(cfg_train: DictConfig):
    import hydra
    from hydra import compose, initialize
    from omegaconf import DictConfig, open_dict
    instantiator = hydra.utils.instantiate
    logger: "SummaryWriter" = instantiator(cfg_train.logger)
    base_datamodule: "BaseDataModule" = hydra.utils.instantiate(cfg_train.dataset)
    criterion = instantiator(cfg_train.loss,)
    net = instantiator(cfg_train.model,)
