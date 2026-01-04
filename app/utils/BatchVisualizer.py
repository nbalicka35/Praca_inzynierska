import matplotlib.pyplot as plt
import numpy as np


class BatchVisualizer:
    """Visualize batches from PyTorch DataLoader"""

    def __init__(
        self, class_names, mean=[0.456, 0.456, 0.456], std=[0.224, 0.224, 0.224]
    ):
        """
        Args:
            class_names: List of class names
        """
        self.class_names = class_names
        self.mean = mean
        self.std = std

    def denormalize(self, tensor):
        """
        Denormalize tensor from training normalization

        Args:
            tensor: Normalized tensor [C, H, W]
            mean: Mean used in normalization
            std: Std used in normalization

        Returns:
            numpy array [H, W, C] with values in [0, 1]
        """
        # Change dimensions [Channel, Height, Width] -> [Height, Width, Channel] and convert to numpy
        img = tensor.permute(1, 2, 0).numpy()

        # Denormalize
        mean = np.array(self.mean)
        std = np.array(self.std)
        img = img * std + mean

        # Clip to [0, 1] range
        img = np.clip(img, 0, 1)

        return img

    def visualize_batch(self, dataloader, total_images=8):
        """
        Visualize a batch of images with their labels

        Args:
            dataloader: PyTorch DataLoader
            num_images: Number of images to display
        """
        imgs, labels = next(iter(dataloader))

        imgs = imgs[:total_images]
        labels = labels[:total_images]
        _, axs = plt.subplots(1, total_images, figsize=(18, 12))

        if total_images == 1:
            axs = [axs]  # Make axs iterable

        for idx in range(total_images):
            img = imgs[idx]
            label = labels[idx].item()

            # Denormalize and convert
            img_denorm = self.denormalize(img)

            axs[idx].imshow(img_denorm)
            axs[idx].set_title(f"{self.class_names[label]}")
            axs[idx].axis("off")

        # Hide unused subplots
        for idx in range(total_images, len(axs)):
            axs[idx].axis("off")

        plt.tight_layout()
        plt.show()

    def visualize_classes(self, dataloader, images_per_class=4):
        """
        Visualize images from each class

        Args:
            dataloader: PyTorch DataLoader
            images_per_class: Number of images to show per class
        """
        classes_count = len(self.class_names)

        class_imgs = {i: [] for i in range(classes_count)}

        for imgs, labels in dataloader:
            for img, label in zip(imgs, labels):
                label_idx = label.item()
                if len(class_imgs[label_idx]) < images_per_class:
                    class_imgs[label_idx].append(img)

            # Check if we have enough images for all classes
            if all(len(imgs) >= images_per_class for imgs in class_imgs.values()):
                break

        _, axs = plt.subplots(
            classes_count,
            images_per_class,
            figsize=(3 * images_per_class, 3 * classes_count),
        )

        for class_idx in range(classes_count):
            for img_idx in range(images_per_class):
                ax = axs[class_idx, img_idx]

                if img_idx < len(class_imgs[class_idx]):
                    img = class_imgs[class_idx][img_idx]
                    img = self.denormalize(img)
                    ax.imshow(img)

                    # Add class name only to first image in row
                    if img_idx == 0:
                        ax.text(
                            -0.15,
                            0.5,
                            self.class_names[class_idx],
                            transform=ax.transAxes,
                            fontsize=14,
                            va="center",
                            ha="right",
                            weight="bold",
                        )

                ax.axis("off")

        plt.suptitle("Sample images from each class", fontsize=22)
        plt.tight_layout()
        plt.subplots_adjust(
            left=0.15,
            wspace=0.05,
            hspace=0.05,
        )
        plt.show()
