import numpy as np


class DatasetStatistics:
    """
    Calculate and display statistical measures for image dataset
    """

    def __init__(self, images=None):
        """
        Initialize with optional list of grayscale images

        Args:
            images: List of numpy arrays (grayscale images)
        """
        self.images = images
        self.stats = None

    def calculate_mean(self):
        """
        Calculate mean pixel intensity across all images

        Returns:
            Float representing mean pixel value
        """
        if self.images is None:
            raise ValueError("No images provided")

        means = []

        for img in self.images:
            means.append(np.mean(img))

        return np.mean(means)

    def calculate_std(self, mean=None):
        """
        Calculate standard deviation of pixel intensities

        Args:
            mean: Pre-calculated mean (optional)

        Returns:
            Float representing standard deviation
        """
        if self.images is None:
            raise ValueError("No images provided")

        if mean is None:
            mean = self.calculate_mean()

        all_pixels = []
        for img in self.images:
            all_pixels.extend(img.flatten())

        all_pixels = np.array(all_pixels)
        return np.std(all_pixels)

    def compute_stats(self):
        """
        Compute comprehensive statistics for the dataset

        Returns:
            Dictionary with mean, std, min, max, median values
        """
        if self.images is None:
            raise ValueError("No images provided")

        mean = self.calculate_mean()
        std = self.calculate_std(mean)

        all_pixels = np.concatenate([img.flatten() for img in self.images])

        self.stats = {
            "mean": mean,
            "std": std,
            "min": np.min(all_pixels),
            "max": np.max(all_pixels),
            "median": np.median(all_pixels),
        }

        return self.stats

    def print_stats(self):
        """Print statistics in a formatted table"""

        if self.stats is None:
            print("Run compute_stats() first")
            return

        print("Dataset Statistics:")
        print(f"\tMean: {self.stats['mean']:.2f}")
        print(f"\tStandard Deviation: {self.stats['std']:.2f}")
        print(f"\tMinimum: {self.stats['min']:.2f}")
        print(f"\tMaximum: {self.stats['max']:.2f}")
        print(f"\tMedian: {self.stats['median']:.2f}")

    def get_normalized_values(self):
        if self.stats is None:
            self.compute_stats()

        return (
            self.stats["mean"] / 255.0,
            self.stats["std"] / 255.0,
        )  # To maintain the [0, 1] scale used in tensors
