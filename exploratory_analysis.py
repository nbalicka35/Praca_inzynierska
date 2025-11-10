import matplotlib.pyplot as plt
import cv2

class DataExplorer:
    def __init__(self, dataset=None):
        self.gray_images = None
        self.data = dataset

    def retrieve_sample_of_images(self, indexes):
        gray_images = []
        for idx in indexes:
            img = self.data[idx]
            img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray_images.append(img)

        self.gray_images = gray_images
        return gray_images

    def plot_histogram(self, bins=16, title=None):
        fig, axs = plt.subplots(2, len(self.gray_images), figsize = (14, 8))
        fig.suptitle(title, fontsize = 20)
        for idx, img in enumerate(self.gray_images):
            axs[0, idx].imshow(img, cmap='gray')
            axs[0, idx].axis('off')

            axs[1, idx].hist(img.flatten(), bins=bins)

        fig.tight_layout()
        plt.show()
