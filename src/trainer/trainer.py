import json
import os
from datetime import datetime
from typing import Iterable

import torch
from tqdm import tqdm

timestamp = datetime.now().strftime("%Y_%m_%d_%Hh%M")


class Trainer:
    def __init__(
        self,
        train_loader,
        val_loader,
        test_loader,
        net,
        logger,
        classes,
        n_epochs: int,
        device,
        log_dir_model: str,
        bool_save_model: bool = True,
        n_epoch_save: int = 1,
        **kwargs,
    ):
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.net = net
        self.logger = logger
        self.classes = classes
        self.device = device
        self.n_epochs = n_epochs
        self.log_dir_model = log_dir_model
        self.n_epoch_save = n_epoch_save
        self.model_checkpoints_dir = os.path.join(self.log_dir_model, "checkpoints")
        self.bool_save_model = bool_save_model
        self.n_classes = len(self.classes)

    def image_label_load(self, data):
        """Utility function for correctly loading data with CUDA."""
        images, labels = data
        images = images.to(self.device)
        labels = labels.to(self.device)
        return images, labels

    def train(self, optimizer, criterion):
        print("---------------MODEL TRAINING---------------")

        for epoch in range(
            1, self.n_epochs + 1
        ):  # loop over the dataset multiple times
            print(f">>>>> Epoch {epoch}")
            running_loss = 0.0
            progress_bar = tqdm(
                enumerate(self.train_loader, 0), total=len(self.train_loader)
            )

            correct_pred = {classname: 0 for classname in self.classes}
            total_pred = {classname: 0 for classname in self.classes}
            self.net.train()
            for _, data in progress_bar:
                inputs, labels = self.image_label_load(data)
                optimizer.zero_grad()
                outputs = self.net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                progress_bar.set_description(f"Epoch: {epoch} - Loss: {loss}")
            # log everything after an epoch.
            self.after_epoch_train_log(running_loss, epoch, correct_pred, total_pred)
            print("Loss for epoch:", running_loss / len(self.train_loader))
            # save model if needs be
            if epoch % self.n_epoch_save == 0 or epoch == self.n_epochs:
                if self.bool_save_model:
                    self.save_model(
                        epoch=epoch, optimizer=optimizer, criterion=criterion
                    )

            self.evaluate_model(epoch)

        print("Finished Training")

    def evaluate_model(self, epoch: int):
        print("---------------MODEL EVALUATION---------------")
        self.net.eval()
        for loader, phase in zip([self.val_loader, self.test_loader], ["val", "test"]):
            correct = 0
            total = 0
            correct_pred = {classname: 0 for classname in self.classes}
            total_pred = {classname: 0 for classname in self.classes}

            with torch.no_grad():
                for data in tqdm(loader, total=len(loader)):
                    images, labels = self.image_label_load(data)
                    outputs = self.net(images)

                    _, predicted = torch.max(outputs.data, 1)
                    predicted = predicted.to(self.device)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                    for label, prediction in zip(labels, predicted):
                        if label == prediction:
                            correct_pred[self.classes[label]] += 1
                        total_pred[self.classes[label]] += 1

            print(f"Accuracy of the network on the images: {100 * correct / total} %")
            accuracy = 100 * correct / total
            self.logger.add_scalar(
                f"total accuracy/{phase}", accuracy, epoch
            ) if self.logger else None

            self.after_epoch_test_log(
                epoch=epoch,
                correct_pred=correct_pred,
                total_pred=total_pred,
                phase=phase,
            )
        self.net.train()

    def save_model(self, epoch: int, optimizer, criterion):
        if not os.path.exists(os.path.join(self.log_dir_model, "checkpoints")):
            os.makedirs(os.path.join(self.log_dir_model, "checkpoints"))
        path_save = os.path.join(
            self.model_checkpoints_dir,
            f"model_{epoch}.pt",
        )
        print("Saving model to", path_save)
        torch.save(
            {
                "epoch": epoch,
                "model_state_dict": self.net.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "criterion": criterion,
            },
            path_save,
        )

    def after_epoch_train_log(self, running_loss, epoch: int, correct_pred, total_pred):
        self.logger.add_scalar(
            "loss/training_loss",
            running_loss / len(self.train_loader),
            epoch,
        ) if self.logger else None
        accuracies = {}
        for classname, correct_count in correct_pred.items():
            if total_pred[classname] == 0:
                continue
            accuracy = 100 * float(correct_count) / total_pred[classname]
            accuracies[classname] = accuracy
        # log accuracy per class on ONE graph
        self.logger.add_scalars(
            f"class_accuracy/train", accuracies, epoch
        ) if self.logger else None
        # log the accuracy per class
        for classname, accuracy_res in accuracies.items():
            self.logger.add_scalar(
                f"class_accuracy/train/{classname}", accuracy_res, epoch
            ) if self.logger else None

    def after_epoch_test_log(
        self, epoch: int, correct_pred, total_pred, phase, metric_report=None
    ):
        # compute accuracy for every class
        accuracies = {}
        for classname, correct_count in correct_pred.items():
            if total_pred[classname] == 0:
                continue
            accuracy = 100 * float(correct_count) / total_pred[classname]
            print(f"Accuracy for class: {classname:5s} is {accuracy:.1f} %")
            accuracies[classname] = accuracy
        # log accuracy per class on ONE graph
        self.logger.add_scalars(
            f"class_accuracy/{phase}", accuracies, epoch
        ) if self.logger else None

        # log the accuracy per class
        for classname, accuracy_res in accuracies.items():
            self.logger.add_scalar(
                f"class_accuracy/{phase}/{classname}", accuracy_res, epoch
            ) if self.logger else None
        if metric_report is not None:
            for classname, metrics in metric_report.items():
                for metric_name, metric in metrics.items():
                    self.logger.add_scalar(
                        f"weighted_class_{metric_name}/{phase}/{classname}",
                        metric.item(),
                        epoch,
                    ) if self.logger else None
