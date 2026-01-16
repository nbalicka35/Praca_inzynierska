from PyQt5.QtWidgets import QApplication


class ScaleManager:
    """
    Scales the interface based on current resolution
    """

    # Set base resolution to 2560x1600
    BASE_WIDTH = 2560
    BASE_HEIGHT = 1600

    def __init__(self):
        self.scale()

    def scale(self):
        """
        Update scale factor
        """
        screen = QApplication.primaryScreen()
        if screen:
            # Get current width and height
            geom = screen.availableGeometry()
            self.width = geom.width()
            self.height = geom.height()

            # Calculate scale factor
            self.scale_x = self.width / self.BASE_WIDTH
            self.scale_y = self.height / self.BASE_HEIGHT
            self.scale = min(self.scale_x, self.scale_y)  # Pick smaller scale factor
            print(f"scale_x: {self.scale_x}\nscale_y: {self.scale_y}")

        else:
            self.scale = 1.0

    def scale_value(self, value):
        """
        Scale given value.
        """
        return int(value * self.scale)

    def scale_size(self, width, height):
        """
        Scale given width & height size.
        """
        return self.scale_value(width), self.scale_value(height)

    def scale_font(self, size):
        """
        Scale font size.
        """
        return max(12, self.scale_value(size))  # Get minimum 12 px up to scaled value
