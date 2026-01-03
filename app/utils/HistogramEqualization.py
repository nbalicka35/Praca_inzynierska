from PIL import ImageOps


class HistogramEqualization:
    def __call__(self, img):
        return ImageOps.equalize(img)
