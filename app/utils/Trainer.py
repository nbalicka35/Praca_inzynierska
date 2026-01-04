import torch
import torch.nn as nn
import time


class Trainer:
    """A training utility class for PyTorch neural network models.
    Handles the complete training loop including forward pass, backpropagation,
    validation, early stopping, and best model checkpoint saving."""

    def __init__(self, model, device, criterion=None):
        """Assign model, device, loss function and history dictonary"""
        self.model = model.to(device)
        self.device = device
        self.criterion = criterion or nn.CrossEntropyLoss()
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
        }

    def train_epoch(self, train_dl, optimizer):
        """Performs one training epoch over the training dataloader.
        Returns tuple of (epoch_loss, epoch_accuracy)."""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for imgs, labels in train_dl:
            imgs, labels = imgs.to(self.device), labels.to(self.device)

            optimizer.zero_grad()
            outs = self.model(imgs)
            loss = self.criterion(outs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * imgs.size(0)
            _, predicted = outs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        epoch_loss = running_loss / total
        epoch_acc = correct / total

        return epoch_loss, epoch_acc

    def validate(self, val_dl):
        """Evaluates model on validation dataloader without gradient computation.
        Returns tuple of (epoch_loss, epoch_accuracy).
        """
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for imgs, labels in val_dl:
                imgs, labels = imgs.to(self.device), labels.to(self.device)

                outs = self.model(imgs)
                loss = self.criterion(outs, labels)

                running_loss += loss.item() * imgs.size(0)
                _, predicted = outs.max(1)
                total += labels.size(0)
                correct += labels.eq(predicted).sum().item()

        epoch_loss = running_loss / total
        epoch_acc = correct / total

        return epoch_loss, epoch_acc

    def fit(self, train_dl, val_dl, optimizer, epochs, patience=5):
        """Complete training loop with early stopping. Monitors validation loss
        and stops training if no improvement is observed for 'patience' epochs.
        Restores best model weights at the end. Returns training history.
        """
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
        }
        count = 0
        start = time.time()

        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(train_dl, optimizer)
            val_loss, val_acc = self.validate(val_dl)

            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)

            if epoch == 0:
                best_val_loss = self.history["val_loss"][epoch]
                best_model_weights = self.model.state_dict().copy()

            else:
                if self.history["val_loss"][epoch] < best_val_loss:
                    best_val_loss = self.history["val_loss"][epoch]
                    best_model_weights = self.model.state_dict().copy()
                    count = 0

                else:
                    count += 1
                    if count > patience:
                        print(f"Early stopping at epoch {epoch+1}")
                        break

            print(
                f"Epoch {epoch+1} out of {epochs} epochs. \
                  \tTrain loss: {train_loss:.4f}, train accuracy: {train_acc:.4f} \
                  \tValidation loss: {val_loss:.4f}, validation accuracy: {val_acc:.4f}"
            )

        total_time = time.time() - start
        print(f"Training completed in {total_time/60:.2f} minute(s)")
        self.model.load_state_dict(best_model_weights)

        return self.history

    def test(self, test_dl):
        self.model.eval()

        correct = 0
        total = 0

        all_predictions = []
        all_labels = []

        with torch.no_grad():
            for imgs, labels in test_dl:
                imgs, labels = imgs.to(self.device), labels.to(self.device)
                outs = self.model(imgs)
                _, predicted = outs.max(1)

                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

            accuracy = correct / total

            return accuracy, all_predictions, all_labels
