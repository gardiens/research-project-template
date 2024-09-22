import random

import numpy as np
import torch
import torchvision
from sklearn.model_selection import train_test_split


class BaseDataModule:
    def __init__(
        self,
        download_cifar,
        batch_size,
        name_classes:"list[str]",
        nb_classes:int,
        num_workers=2,
        path_data:str="./data"
    ):
        self.download_cifar = download_cifar

        self.path_data=path_data
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.name_classes=name_classes
        self.nb_classes=nb_classes
    def get_dataset(self, transform_train):
        train_dataset_full = torchvision.datasets.CIFAR10(
            root=self.path_data,
            train=True,
            download=self.download_cifar,
            transform=transform_train,
        )
        train_targets = train_dataset_full.targets

        target_indices = np.arange(len(train_targets))
        train_idx, val_idx = train_test_split(target_indices, train_size=0.8)


        train_dataset = torch.utils.data.Subset(train_dataset_full, train_idx)
        train_loader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )

        # get val dataset
        val_dataset = torch.utils.data.Subset(train_dataset_full, val_idx)
        val_loader = torch.utils.data.DataLoader(
            val_dataset, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers
        )

        # get test dataset
        test_dataset_full = torchvision.datasets.CIFAR10(
            root=self.path_data,
            train=False,
            download=self.download_cifar,
            transform=transform_train,
        )
        indices_test = np.arange(len(test_dataset_full.targets))
        test_dataset = torch.utils.data.Subset(test_dataset_full, indices_test)
        test_loader = torch.utils.data.DataLoader(
            test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
        )

     
        return train_loader, val_loader, test_loader
