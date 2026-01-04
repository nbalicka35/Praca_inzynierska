import cv2
import matplotlib.pyplot as plt


class DataExplorer:
    """Visualize dataset samples with histograms"""

    def __init__(self, file_paths=None):
        self.file_paths = file_paths
        self.gray_images = None

    def retrieve_sample_of_images(self, indexes, equalize=False):
        """
        Load sample images at given indexes

        Args:
            indexes: List of image indexes to load

        Returns:
            List of grayscale images
        """

        gray_images = []

        for idx in indexes:
            img_path = self.file_paths[idx]
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if equalize:
                img = cv2.equalizeHist(img)

            gray_images.append(img)

        self.gray_images = gray_images

    def plot_histogram(self, bins=32, title=None):
        """
        Plot images with their pixel intensity histograms

        Args:
            bins: Number of histogram bins
            title: Figure title
        """

        if self.gray_images is None:
            raise ValueError("Retrieve sample images first")

        n_images = len(self.gray_images)
        fig, axs = plt.subplots(2, n_images, figsize=(14, 8))

        if title:
            fig.suptitle(title, fontsize=20)

        for idx, img in enumerate(self.gray_images):
            # Display image
            axs[0, idx].imshow(img, cmap="gray")
            axs[0, idx].axis("off")
            axs[0, idx].set_title(f"Image {idx + 1}")

            # Display corresponding histogram
            axs[1, idx].hist(
                img.flatten(), bins=bins, color="lightblue", alpha=0.8, edgecolor="blue"
            )
            axs[1, idx].set_xlabel("Pixel intensity value (0 - 255)", fontsize=10)
            axs[1, idx].set_ylabel("Frequency", fontsize=10)
            axs[1, idx].grid(alpha=0.3)
            axs[1, idx].set_xlim([0, 255])

        fig.tight_layout()
        plt.show()
