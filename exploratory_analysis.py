import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

class DataExplorer:
    def __init__(self, dataset=None):
        self.images = None
        self.data = dataset

    def retrieve_sample_of_images(self, indexes):
        images = []
        for idx in indexes:
            img = self.data[idx]
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            images.append(img)

        self.images = images
        return images

    def plot_histogram(self, bins=16, title=None):
        fig, axs = plt.subplots(2, len(self.images), figsize = (14, 8))
        fig.suptitle(title, fontsize = 20)
        for idx, img in enumerate(self.images):
            axs[0, idx].imshow(img, cmap='gray')
            axs[0, idx].axis('off')

            axs[1, idx].hist(img.flatten(), bins=bins)

        fig.tight_layout()
        plt.show()
