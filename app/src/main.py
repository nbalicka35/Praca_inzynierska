import os
import sys

# Project directories
current_dir = os.path.dirname(os.path.abspath(__file__))  # app/src
app_dir = os.path.dirname(current_dir)  # app
project_dir = os.path.dirname(app_dir)  # Praca_inzynierska
utils_dir = os.path.join(app_dir, "utils")

# checkpoint's dir
CHECKPOINT_PATH = os.path.join(project_dir, "config", "resnet34.pth")

sys.path.insert(0, utils_dir)

# Import PyTorch (przed PyQt5)
from BrainTumorClassifier import BrainTumorClassifier
from GradCAM import generate_gradcam
import ErrMsgDialog

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
    QScrollArea,
    QProgressBar,
    QDialog,
)
import numpy as np
import cv2
from PIL import Image
from PyQt5.QtCore import QSize, QStandardPaths, Qt
from PyQt5.QtGui import QPixmap, QImage
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
        self.classifier = BrainTumorClassifier(CHECKPOINT_PATH)

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
        self.results_card = QScrollArea()
        self.results_card.setObjectName("results_card")
        self.results_card.setWidgetResizable(True)
        self.results_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.results_card.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_card.setStyleSheet(
            """
            #results_card {
                background-color: rgba(148, 211, 255, .2);
                border-radius: 10px;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(148, 211, 255, .1);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(148, 211, 255, .5);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
        )
        self.results_card.setMinimumHeight(300)

        self.results_container = QWidget()
        self.results_container.setStyleSheet("background-color: transparent;")
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(15, 15, 15, 15)
        self.results_layout.setSpacing(10)
        self.results_layout.setAlignment(Qt.AlignTop)

        self.results_card.setWidget(self.results_container)

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
        """
        Runs prediction for uploaded data.
        """
        if not self.predict_enabled:
            return

        self.predict_button.setText("Thinking...")
        self.clear_button.setEnabled(False)

        # Refresh app before long processing operation
        QApplication.processEvents()
        print(f"selected_file: {self.selected_file}")
        print(f"selected_files: {self.selected_files}")
        try:
            if self.selected_file:
                res = self.classifier.predict(self.selected_file)
                self.show_single_res(res)

            elif self.selected_files:
                res = self.classifier.predict_batch(self.selected_files)
                self.show_batch_res(res)

        except Exception as e:
            ErrMsgDialog(parent=self, title="Prediction failed", msg=e)
            print(f"Prediction error: {e}")

        finally:
            self.predict_button.setText("Predict")
            self.predict_button.setEnabled(True)
            self.clear_button.setEnabled(True)

    def show_single_res(self, res):
        """
        Display prediction for one image.
        """
        self.clear_results()

        card = self.create_res_card(
            filename=os.path.basename(self.selected_file),
            filepath=self.selected_file,
            pred=res["class_name"],
            confidence=res["confidence"],
        )
        self.results_layout.addWidget(card)
        self.results_layout.addStretch()

    def show_batch_res(self, res):
        """
        Display prediction for many images.
        """
        self.clear_results()

        for result in res:
            card = self.create_res_card(
                filename=os.path.basename(result["filepath"]),
                filepath=result["filepath"],
                pred=result["class_name"],
                confidence=result["confidence"],
            )
            self.results_layout.addWidget(card)

        self.results_layout.addStretch()

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
        self.update_confidence_bar_visibility()

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

        self.clear_results()

    def create_res_card(self, filepath, filename, pred, confidence):
        """
        Create colorful result card for the pred.
        """
        colors = {
            "glioma_tumor": "#DA5F62",
            "meningioma_tumor": "#F0B880",
            "no_tumor": "#93F080",
            "pituitary_tumor": "#F0F47A",
        }

        card_color = colors[pred]

        card = QWidget()
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet(
            f"""
            QWidget {{
                background-color: {card_color};
                border-radius: 15px;
                font-size: 14px;
            }}
            """
        )
        card.setFixedHeight(50)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        name_label = QLabel(filename)
        name_label.setStyleSheet(f"background-color: transparent; border: none;")
        name_label.setFixedWidth(120)
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        class_label = QLabel(pred.replace("_", " ").title())
        class_label.setStyleSheet(
            f"background-color: transparent; border: none; font-weight: bold;"
        )
        class_label.setFixedWidth(140)
        class_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Confidence bar
        confidence_bar = QProgressBar(card)
        confidence_bar.setFixedSize(120, 15)
        confidence_bar.setMinimum(0)
        confidence_bar.setMaximum(100)
        confidence_bar.setValue(int(confidence * 100))
        confidence_bar.setTextVisible(False)
        confidence_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #D8D8D8;
                border-radius: 2px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #94D3FF;
                border-radius: 2px;
            }
        """
        )
        confidence_bar.setVisible(self.width() >= 1400)

        conf_label = QLabel(f"{confidence*100:.2f}% confidence")
        conf_label.setStyleSheet(f"background-color: transparent; border: none;")
        conf_label.setFixedWidth(130)
        conf_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        details_button = QPushButton("🔍")
        details_button.setFixedSize(30, 30)
        details_button.setCursor(Qt.PointingHandCursor)
        details_button.setToolTip("Show GradCAM visualization")
        details_button.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 15px;
            }
        """
        )
        details_button.clicked.connect(
            lambda checked, f=filepath: self.show_gradcam_window(f)
        )

        layout.addWidget(name_label)
        layout.addWidget(class_label)
        layout.addStretch()
        layout.addWidget(confidence_bar)
        layout.addWidget(conf_label)
        layout.addWidget(details_button)

        card.confidence_bar = confidence_bar

        return card

    def update_confidence_bar_visibility(self):
        show_bars = self.width() >= 1400

        for i in range(self.results_layout.count()):
            item = self.results_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                # Check if card has confidence attribute
                if hasattr(card, "confidence_bar"):
                    card.confidence_bar.setVisible(show_bars)

    def show_gradcam_window(self, filepath):
        self.setCursor(Qt.WaitCursor)

        try:
            img_pil = Image.open(filepath).convert("RGB")
            if img_pil is None:
                print(f"Could not load the image: {filepath}")
                self.setCursor(Qt.ArrowCursor)
                return

            img_resized = img_pil.resize(self.classifier.image_size)
            img_np = np.array(img_resized)

            img_trans = self.classifier.transform(img_pil)
            img_tensor = img_trans.unsqueeze(0).to(self.classifier.device)

            res = generate_gradcam(
                model=self.classifier.model,
                img_tensor=img_tensor,
                original_img=img_np,
                device=self.classifier.device,
            )

            original_pixmap = self.rgb_to_pixmap(img_np)
            heatmap_pixmap = self.rgb_to_pixmap(
                cv2.cvtColor(res["heatmap"], cv2.COLOR_BGR2RGB)
            )
            superimposed_pixmap = self.rgb_to_pixmap(
                cv2.cvtColor(res["superimposed"], cv2.COLOR_BGR2RGB)
            )

            gradcam_dialog = QDialog(self)
            gradcam_dialog.setWindowTitle(f"GradCAM for {os.path.basename(filepath)}")
            gradcam_dialog.setMinimumSize(600, 300)

            gradcam_layout = QVBoxLayout(gradcam_dialog)
            images_layout = QHBoxLayout()

            original_container = QVBoxLayout()
            original_label = QLabel(f"Original {os.path.basename(filepath)}")
            original_label.setAlignment(Qt.AlignCenter)
            original_label.setStyleSheet("font-weight: bold;")
            original_img = QLabel()
            original_img.setPixmap(
                original_pixmap.scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            original_img.setAlignment(Qt.AlignCenter)
            original_container.addWidget(original_label)
            original_container.addWidget(original_img)

            heatmap_container = QVBoxLayout()
            heatmap_label = QLabel("GradCAM Heatmap")
            heatmap_label.setAlignment(Qt.AlignCenter)
            heatmap_label.setStyleSheet("font-weight: bold;")
            heatmap_img = QLabel()
            heatmap_img.setPixmap(
                heatmap_pixmap.scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            heatmap_img.setAlignment(Qt.AlignCenter)
            heatmap_container.addWidget(heatmap_label)
            heatmap_container.addWidget(heatmap_img)

            superimposed_container = QVBoxLayout()
            superimposed_label = QLabel("Overlay")
            superimposed_label.setAlignment(Qt.AlignCenter)
            superimposed_label.setStyleSheet("font-weight: bold;")
            superimposed_img = QLabel()
            superimposed_img.setPixmap(
                superimposed_pixmap.scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
            superimposed_img.setAlignment(Qt.AlignCenter)
            superimposed_container.addWidget(superimposed_label)
            superimposed_container.addWidget(superimposed_img)

            images_layout.addLayout(original_container)
            images_layout.addLayout(heatmap_container)
            images_layout.addLayout(superimposed_container)

            info_label = QLabel(
                f"Prediction: {self.classifier.classes[res["class_index"]].replace("_", " ").title()} ({res["confidence"]*100:.2f}%)"
            )
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setStyleSheet("font-size: 16px; margin-top: 10px;")

            gradcam_layout.addLayout(images_layout)
            gradcam_layout.addWidget(info_label)

            self.setCursor(Qt.ArrowCursor)
            gradcam_dialog.exec()

        except Exception as e:
            ErrMsgDialog(parent=self, title="Visualization error has occured.", msg=e)
            print(f"GradCAM error: {e}")
            self.setCursor(Qt.ArrowCursor)

    def rgb_to_pixmap(self, rgb_img):
        height, width, channel = rgb_img.shape
        bytes_per_line = width * channel

        qimg = QImage(rgb_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg.copy())

    def clear_results(self):
        """
        Clears results card.
        """
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                pass


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
