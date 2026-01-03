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
    QSizePolicy,
)
from PyQt5.QtCore import QSize, QStandardPaths, Qt
from PyQt5.QtGui import QPixmap
from TopBar import TopBar


class StepLabel(QLabel):
    def __init__(self, step):
        super().__init__()
        self.setText(f"Step {step}")
        self.setStyleSheet("font-weight: bold;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.selected_files = []
        self.selected_directory = None
        self.predict_enabled = False

        # Window properties
        self.setWindowTitle("Neuron Desktop App")
        self.setMinimumSize(QSize(1280, 720))

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #FFFAF2;")

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

        # Buttons styles
        button_style = """
            QPushButton {
                background-color: rgba(148, 211, 255, .72);
                border: 0px;
                border-radius: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(148, 211, 255, .9);
            }
        """
        BUTTON_WIDTH = 150
        BUTTON_HEIGHT = 45

        # Step 1
        step1_label = QLabel("Step 1")
        step1_label.setStyleSheet(
            "font-weight: bold; font-size: 18px; background-color:white;"
        )
        step1_desc = QLabel("Select .jpg file or directory")
        step1_desc.setStyleSheet("font-size: 16px; background-color:white;")

        # Choice buttons
        buttons_layout = QHBoxLayout()
        self.file_button = QPushButton("Choose file")
        self.file_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.file_button.setStyleSheet(button_style)
        self.file_button.setCursor(Qt.PointingHandCursor)
        self.file_button.clicked.connect(self.open_file)

        self.dir_button = QPushButton("Choose directory")
        self.dir_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.dir_button.setStyleSheet(button_style)
        self.dir_button.setCursor(Qt.PointingHandCursor)
        self.dir_button.clicked.connect(self.open_directory)

        buttons_layout.addWidget(self.file_button)
        buttons_layout.addWidget(self.dir_button)
        buttons_layout.addStretch()

        self.preview_label = QLabel("Preview of selected image(s) will appear below")
        self.preview_label.setStyleSheet("background-color:white;")

        self.preview_container = QWidget()
        self.preview_container.setStyleSheet("background-color: white;")
        self.preview_container.setVisible(False)

        preview_container_layout = QVBoxLayout(self.preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)
        preview_container_layout.setSpacing(10)

        self.file_name_label = QLabel("")
        self.file_name_label.setStyleSheet("background-color: white; font-size: 12px;")

        image_row = QHBoxLayout()
        image_row.setAlignment(Qt.AlignLeft)
        image_row.setSpacing(10)

        self.thumbnails_container = QWidget()
        self.thumbnails_container.setStyleSheet("background-color: white;")
        self.thumbnails_layout = QHBoxLayout(self.thumbnails_container)
        self.thumbnails_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnails_layout.setSpacing(10)
        self.thumbnails_layout.setAlignment(Qt.AlignLeft)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.clear_button.setStyleSheet(button_style)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_selection)
        self.clear_button.setEnabled(False)

        image_row.addWidget(self.thumbnails_container)
        image_row.addSpacing(20)
        image_row.addWidget(self.clear_button, alignment=Qt.AlignBottom)
        image_row.addStretch()

        preview_container_layout.addWidget(self.file_name_label)
        preview_container_layout.addLayout(image_row)

        # Step 2
        step2_label = QLabel("Step 2")
        step2_label.setStyleSheet(
            "font-weight: bold; font-size: 18px; background-color:white;"
        )
        step2_desc = QLabel("Examine photo(s)")
        step2_desc.setStyleSheet("font-size: 16px; background-color:white;")

        # Predict button
        predict_layout = QHBoxLayout()
        self.predict_button = QPushButton("Predict")
        self.predict_button.setEnabled(self.predict_enabled)
        self.predict_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.predict_button.setStyleSheet(button_style)
        self.predict_button.setCursor(Qt.PointingHandCursor)
        self.predict_button.clicked.connect(self.predict)
        predict_layout.addWidget(self.predict_button)
        predict_layout.addStretch()

        # Disclaimer
        disclaimer_layout = QHBoxLayout()
        disclaimer_layout.setAlignment(Qt.AlignLeft)
        disclaimer_layout.setSpacing(5)

        disclaimer_icon = QLabel("⚠️")
        disclaimer_icon.setStyleSheet("background-color: white;")
        disclaimer_icon.setAlignment(Qt.AlignTop)

        disclaimer_text = QLabel(
            "Please note that Neuron is a software designed to support physicians and radiologists, and can make mistakes.\n"
            "Always examine patients and make a decision based on the knowledge of yours."
        )
        disclaimer_text.setStyleSheet("background-color: white;")
        disclaimer_text.setAlignment(Qt.AlignLeft)

        disclaimer_layout.addWidget(disclaimer_icon)
        disclaimer_layout.addWidget(disclaimer_text)
        disclaimer_layout.addStretch()

        left_column.addWidget(step1_label)
        left_column.addWidget(step1_desc)
        left_column.addLayout(buttons_layout)
        left_column.addWidget(self.preview_label)
        left_column.addWidget(self.preview_container)
        left_column.addSpacing(20)
        left_column.addWidget(step2_label)
        left_column.addWidget(step2_desc)
        left_column.addLayout(predict_layout)
        left_column.addStretch()
        left_column.addLayout(disclaimer_layout)

        # Right column inside the card
        right_column = QVBoxLayout()
        right_column.setAlignment(Qt.AlignTop)

        step3_label = QLabel("Step 3")
        step3_label.setStyleSheet(
            "font-weight: bold; font-size: 18px; background-color: white;"
        )
        step3_desc = QLabel("Check the result for the photo(s) below")
        step3_desc.setStyleSheet("font-size: 16px; background-color:white;")

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
            self, "Open File", pictures_path, "JPG files (*.jpg *.jpeg)"
        )

        if filename:
            self.selected_file = filename
            self.selected_files = []

            self.preview_label.setVisible(False)
            self.preview_container.setVisible(True)

            file_name = os.path.basename(filename)
            self.file_name_label.setText(f"Selected: {file_name}")

            self.clear_thumbnails()
            self.add_thumbnail(filename)

            self.predict_enabled = True
            self.predict_button.setEnabled(self.predict_enabled)
            self.clear_button.setVisible(True)
            self.clear_button.setEnabled(True)
            print(f"{filename} loaded.")

    def open_directory(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select Folder")

        if not dirname:
            return

        jpg_files = []
        if os.path.exists(dirname) and os.path.isdir(dirname):
            for filename in os.listdir(dirname):
                if filename.lower().endswith((".jpg", ".jpeg")):
                    filepath = os.path.join(dirname, filename)
                    if os.path.isfile(filepath):
                        jpg_files.append(filepath)

        self.preview_label.setVisible(False)
        self.preview_container.setVisible(True)
        self.clear_thumbnails()

        if jpg_files:
            self.selected_file = None
            self.selected_files = jpg_files
            self.selected_directory = dirname

            self.preview_label.setVisible(False)
            self.preview_container.setVisible(True)

            self.file_name_label.setText(
                f"Selected {len(jpg_files)} images from {os.path.basename(dirname)}"
            )

            self.clear_thumbnails()
            self.show_directory_preview(jpg_files)

            self.clear_button.setVisible(True)
            self.clear_button.setEnabled(True)

            self.predict_enabled = True
            self.predict_button.setEnabled(self.predict_enabled)
        else:
            self.selected_files = []
            self.selected_directory = None

            self.file_name_label.setText(
                f"No .jpg files found in {os.path.basename(dirname)}"
            )
            self.predict_enabled = False
            self.predict_button.setEnabled(self.predict_enabled)
            self.clear_button.setVisible(False)
            self.clear_thumbnails()

    def predict(self):
        self.predict_button.setText("Thinking...")
        self.clear_button.setEnabled(False)

    def change_theme(self):
        if self.theme_button.isChecked():
            self.theme_button.setText("Dark")

        else:
            self.theme_button.setText("Light")

    def clear_selection(self):
        # Clear chosen files
        self.selected_file = None
        self.selected_files = []
        self.selected_directory = None

        self.preview_label.setVisible(True)
        self.preview_container.setVisible(False)

        self.file_name_label.setText("")
        self.clear_thumbnails()

        self.predict_enabled = False
        self.predict_button.setEnabled(self.predict_enabled)

        self.clear_button.setVisible(True)
        self.clear_button.setEnabled(False)
        print("Selection cleared.")

    def get_preview_size(self):
        window_height = self.height()
        preview_size = int(window_height * 0.15)
        return max(80, min(preview_size, 150))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_thumbnails_size()

    def update_thumbnails_size(self):
        preview_size = self.get_preview_size()

        for i in range(self.thumbnails_layout.count()):
            widget = self.thumbnails_layout.itemAt(i).widget()
            if widget:
                widget.setFixedSize(preview_size, preview_size)

                # If filepath present, reload
                filepath = widget.property("filepath")
                if filepath:
                    pixmap = QPixmap(filepath)
                    if not pixmap.isNull():
                        scaled = pixmap.scaled(
                            preview_size,
                            preview_size,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation,
                        )
                        widget.setPixmap(scaled)

    def show_directory_preview(self, filepaths, number_of_previews=3):
        for filepath in filepaths[:number_of_previews]:
            self.add_thumbnail(filepath)

        if len(filepaths) > number_of_previews:
            more_label = QLabel(f"+{len(filepaths) - number_of_previews}")
            more_label.setStyleSheet(
                """
                background-color: rgba(148, 211, 255, .3);
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            """
            )
            more_label.setAlignment(Qt.AlignCenter)
            more_label.setFixedSize(self.get_preview_size(), self.get_preview_size())
            more_label.setObjectName("more_label")
            self.thumbnails_layout.addWidget(more_label)

    def add_thumbnail(self, filepath):
        thumbnail = QLabel()
        thumbnail.setStyleSheet("background-color: white;")
        thumbnail.setAlignment(Qt.AlignCenter)
        thumbnail.setObjectName("thumbnail")

        preview_size = self.get_preview_size()
        thumbnail.setFixedSize(preview_size, preview_size)

        pixmap = QPixmap(filepath)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                preview_size, preview_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            thumbnail.setPixmap(scaled)

        # Save filepath as a property of the thumbnail for refresh overhead
        thumbnail.setProperty("filepath", filepath)

        self.thumbnails_layout.addWidget(thumbnail)

    def clear_thumbnails(self):
        while self.thumbnails_layout.count():
            item = self.thumbnails_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
