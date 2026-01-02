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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.top_bar = TopBar()

        self.card = QWidget()
        self.card.setObjectName("card")
        self.card.setStyleSheet(
            """
            #card {
                background-color: white;
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            }
        """
        )

        self.card_layout = QHBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 30, 30, 30)

        left_column = QVBoxLayout()

        self.step1 = StepLabel(1)
        self.file_label = QLabel("Choose a .jpg file or directory")

        self.file_button = QPushButton("Choose file")
        self.file_button.setMaximumSize(210, 45)
        self.file_button.clicked.connect(self.open_file)

        self.dir_button = QPushButton("Choose directory")
        self.dir_button.setMinimumSize(210, 45)
        self.dir_button.clicked.connect(self.open_directory)

        left_column.addWidget(self.step1)
        left_column.addWidget(self.file_label)
        left_column.addWidget(self.file_button)
        left_column.addWidget(self.dir_button)

        self.step2 = StepLabel(2)
        self.p_label = QLabel("Click the button below")

        self.predict_button = QPushButton("Predict")
        self.predict_button.setMaximumSize(210, 45)
        self.predict_button.setEnabled(self.predict_enabled)
        self.predict_button.clicked.connect(self.predict)

        left_column.addWidget(self.step2)
        left_column.addWidget(self.p_label)
        left_column.addWidget(self.predict_button)

        right_column = QVBoxLayout()

        self.step3 = StepLabel(3)
        self.r_label = QLabel("Read the result")

        right_column.addWidget(self.step3)
        right_column.addWidget(self.r_label)

        self.card_layout.addLayout(left_column)
        self.card_layout.addLayout(right_column)

        card_wrapper = QWidget()
        card_wrapper_layout = QVBoxLayout(card_wrapper)
        card_wrapper_layout.setContentsMargins(30, 60, 30, 0)
        card_wrapper_layout.addWidget(self.card)

        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(card_wrapper, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
