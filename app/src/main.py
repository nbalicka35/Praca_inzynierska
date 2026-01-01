import os
import sys


# Ustaw ścieżkę do pluginów Qt przed importem PyQt5 (przypadek dla środowiska wirtualnego)
pyqt_path = os.path.join(sys.prefix, "Lib", "site-packages", "PyQt5", "Qt5", "plugins")
os.environ["QT_PLUGIN_PATH"] = pyqt_path

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtCore import QSize, QStandardPaths


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neuron Desktop App")
        self.setMinimumSize(QSize(1280, 720))

        self.c_button = QPushButton("Choose a file")
        self.c_button.clicked.connect(self.open_file)

        self.p_button = QPushButton("Predict")
        self.p_button.clicked.connect(self.predict)

        self.setCentralWidget(self.c_button)

    def open_file(self):
        pictures_path = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", pictures_path, "JPG files (*.jpg)"
        )

        if filename:
            self.c_button.setText(f"{filename} loaded.")

    def predict(self):
        print("Prediction in progress...")
        self.p_button.setText("Prediction in progress...")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
