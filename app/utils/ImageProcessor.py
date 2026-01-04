import cv2
import matplotlib.pyplot as plt
import numpy as np


class ImageProcessor:
    """Handles image loading, conversion, and analysis operations"""

    def __init__(self, file_paths=None):
        self.file_paths = file_paths
        self.gray_images = None

    def load_grayscale_images(self, equalize=False):
        """
        Load all images and convert to grayscale
        """
        if self.file_paths is None:
            raise ValueError("No file paths provided")

        gray_images = []
        total = len(self.file_paths)

        print(f"Loading {total} images and converting to grayscale...")

        for i, filepath in enumerate(self.file_paths):
            if (i + 1) % 500 == 0 or i == 0:
                print(f"  Progress: {i + 1}/{total} images")

            img = cv2.imread(filepath)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if equalize:
                gray_img = cv2.equalizeHist(gray_img)

            gray_images.append(gray_img)

        self.gray_images = gray_images
        print("Images loaded")

    def display_image_grid(self, batch_size=64, images_per_row=8, figsize=(12, 12)):
        """
        Display a grid of loaded grayscale images

        Args:
            batch_size: Total number of images to display
            images_per_row: Number of images per row
            figsize: Figure size in inches
        """
        if self.gray_images is None:
            raise ValueError(
                "Load grayscale images first using load_grayscale_images()"
            )

        batch_size = min(batch_size, len(self.gray_images))
        n_rows = int(np.ceil(batch_size / images_per_row))

        fig, axs = plt.subplots(n_rows, images_per_row, figsize=figsize)
        fig.suptitle(f"{batch_size} MRI Brain Tumor Images", fontsize=20)

        for row in range(n_rows):
            for col in range(images_per_row):
                idx = row * images_per_row + col

                if idx >= batch_size:
                    axs[row][col].axis("off")
                    continue

                img = self.gray_images[idx]
                axs[row][col].imshow(img, cmap="gray", aspect="equal")
                axs[row][col].axis("off")

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.tight_layout()
        plt.show()
