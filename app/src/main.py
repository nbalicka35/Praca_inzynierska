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

        # Window properties
        self.setWindowTitle("Neuron Desktop App")
        self.setMinimumSize(QSize(1280, 720))

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #FFFAF2;")

        self.predict_enabled = False

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
        self.top_bar = TopBar()
        self.top_bar.setContentsMargins(0, 0, 0, 50)

        # White card
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
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)

        # Left column inside the card
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignTop)

        # Step 1
        step1_label = QLabel("Step 1")
        step1_label.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color:white;"
        )
        step1_desc = QLabel("Select .jpg file or directory")
        step1_desc.setStyleSheet("background-color:white;")

        # Choice buttons
        buttons_layout = QHBoxLayout()
        self.file_button = QPushButton("Choose file")
        self.dir_button = QPushButton("Choose directory")
        self.file_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(148, 211, 255, .72);
                border: 0px;
                border-radius: 10px;
                padding: 15px 40px;
            }
            """
        )
        self.dir_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(148, 211, 255, .72);
                border: 0px;
                border-radius: 10px;
                padding: 15px 40px;
            }
            """
        )

        buttons_layout.addWidget(self.file_button)
        buttons_layout.addWidget(self.dir_button)
        buttons_layout.addStretch()

        self.preview_label = QLabel("Preview of selected image(s) will appear below")
        self.preview_label.setStyleSheet("background-color:white;")

        # Step 2
        step2_label = QLabel("Step 2")
        step2_label.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color:white;"
        )
        step2_desc = QLabel("Examine photo(s)")
        step2_desc.setStyleSheet("background-color:white;")
        self.predict_button = QPushButton("Predict")
        self.predict_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(148, 211, 255, .72);
                border: 0px;
                border-radius: 10px;
                padding: 15px 0px;
            }
            """
        )

        left_column.addWidget(step1_label)
        left_column.addWidget(step1_desc)
        left_column.addLayout(buttons_layout)
        left_column.addWidget(self.preview_label)
        left_column.addSpacing(30)
        left_column.addWidget(step2_label)
        left_column.addWidget(step2_desc)
        left_column.addWidget(self.predict_button)
        left_column.addStretch()

        # Right column inside the card
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignTop)

        step3_label = QLabel("Step 3")
        step3_label.setStyleSheet(
            "font-weight: bold; font-size: 16px; background-color: white;"
        )
        step3_desc = QLabel("Check the result for the photo(s) below")
        step3_desc.setStyleSheet("background-color:white;")

        # Result(s) panel
        self.results_card = QWidget()
        self.results_card.setObjectName("results_card")
        self.results_card.setStyleSheet(
            """
            #results_card {
                background-color: rgba(148, 211, 255, .2);
                border-radius: 10px;
            }
            """
        )
        self.results_card.setMinimumHeight(300)

        right_column.addWidget(step3_label)
        right_column.addWidget(step3_desc)
        right_column.addWidget(self.results_card, 1)

        # Add columns to the card
        self.card_layout.addLayout(left_column, 1)
        self.card_layout.addLayout(right_column, 1)

        # Wrapper + margins
        card_wrapper = QWidget()
        card_wrapper.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        card_wrapper_layout = QVBoxLayout(card_wrapper)
        card_wrapper_layout.setContentsMargins(20, 0, 20, 0)
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
