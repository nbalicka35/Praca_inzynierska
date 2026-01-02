import os
import sys


# Ustaw ścieżkę do pluginów Qt przed importem PyQt5 (przypadek dla środowiska wirtualnego)
pyqt_path = os.path.join(sys.prefix, "Lib", "site-packages", "PyQt5", "Qt5", "plugins")
os.environ["QT_PLUGIN_PATH"] = pyqt_path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
)
from PyQt5.QtCore import QSize, QStandardPaths, Qt
from TopBar import TopBar


class StepLabel(QLabel):
    def __init__(self, step):
        super().__init__()
        self.setText(f"Step {step}")
        self.setStyleSheet("font-weight: bold;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #FFFAF2;")

        self.predict_enabled = False

        self.setWindowTitle("Neuron Desktop App")
        self.setMinimumSize(QSize(1280, 720))

        layout = QVBoxLayout()

        self.top_bar = TopBar()

        self.step1 = StepLabel(1)
        self.file_label = QLabel("Choose a .jpg file or directory")

        self.file_button = QPushButton("Choose file")
        self.file_button.setMaximumSize(210, 45)
        self.file_button.clicked.connect(self.open_file)

        self.dir_button = QPushButton("Choose directory")
        self.dir_button.setMinimumSize(210, 45)
        self.dir_button.clicked.connect(self.open_directory)

        ch_layout = QHBoxLayout()
        ch_layout.addWidget(self.file_button)
        ch_layout.addWidget(self.dir_button)
        ch_widget = QWidget()
        ch_widget.setLayout(ch_layout)

        self.step2 = StepLabel(2)
        self.p_label = QLabel("Click the button below")

        self.predict_button = QPushButton("Predict")
        self.predict_button.setMaximumSize(210, 45)
        self.predict_button.setEnabled(self.predict_enabled)
        self.predict_button.clicked.connect(self.predict)

        self.step3 = StepLabel(3)
        self.r_label = QLabel("Read the result")

        layout.addWidget(self.top_bar)
        layout.addWidget(self.step1)
        layout.addWidget(self.file_label)
        layout.addWidget(ch_widget)
        layout.addWidget(self.step2)
        layout.addWidget(self.p_label)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.step3)
        layout.addWidget(self.r_label)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def open_file(self):
        pictures_path = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", pictures_path, "JPG files (*.jpg)"
        )

        if filename:
            print(f"{filename} loaded.")
            self.predict_enabled = True
            self.predict_button.setEnabled(self.predict_enabled)

    def open_directory(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select Folder")

        if dirname:
            self.dir_button.setText(dirname)
            self.predict_enabled = True
            self.predict_button.setEnabled(self.predict_enabled)

    def predict(self):
        print("Prediction in progress...")
        self.predict_button.setText("Prediction in progress...")

    def change_theme(self):
        if self.theme_button.isChecked():
            self.theme_button.setText("Dark")

        else:
            self.theme_button.setText("Light")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
