from PyQt5.QtWidgets import QApplication


class ScaleManager:
    """
    Scales the interface based on current resolution
    """

    # Base resolution (1080p as reference)
    BASE_HEIGHT = 1080
    BASE_PIXEL_RATIO = 1.0

    def __init__(self):
        self.scale()

    def scale(self):
        """
        Update scale factor based on screen properties
        """
        screen = QApplication.primaryScreen()
        if screen:
            # Get current width and height
            geom = screen.availableGeometry()
            self.width = geom.width()
            self.height = geom.height()

            # Get device pixel ratio (including windows scaling)
            self.pixel_ratio = screen.devicePixelRatio()
            # Scale in regard of base 1080p res
            resolution_scale = self.height / self.BASE_HEIGHT
            # DPI compensation
            self.scale_factor = resolution_scale / self.pixel_ratio

            if self.width >= 2560:
                self.scale_factor *= 1
            elif self.width >= 1920:
                self.scale_factor *= 0.8

            # Restrict scale factor range (0.6 - 1.8)
            self.scale_factor = max(0.6, min(1.8, self.scale_factor))

        else:
            self.scale_factor = 1.0

    def scale_value(self, value):
        """
        Scale given value.
        """
        return int(value * self.scale_factor)

    def scale_size(self, width, height):
        """
        Scale given width & height size.
        """
        return self.scale_value(width), self.scale_value(height)

    def scale_font(self, size):
        """
        Scale font size.
        """
        return max(10, self.scale_value(size))  # Get minimum 10 px up to scaled value
