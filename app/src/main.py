import os
import sys

# Project directories
current_dir = os.path.dirname(os.path.abspath(__file__))  # app/src
app_dir = os.path.dirname(current_dir)  # app
project_dir = os.path.dirname(app_dir)  # Praca_inzynierska
utils_dir = os.path.join(app_dir, "utils")

# Checkpoint's dir (file with model parameters)
CHECKPOINT_PATH = os.path.join(project_dir, "config", "resnet34.pth")

sys.path.insert(0, utils_dir)

from BrainTumorClassifier import BrainTumorClassifier
from GradCAM import generate_gradcam

# Set the Qt plugins' directory before Qt5 import (case for virtual environment)
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
    QProgressBar,
    QDialog,
    QMessageBox,
)
from PyQt5.QtCore import QSize, QStandardPaths, Qt
from PyQt5.QtGui import QPixmap, QImage

import numpy as np
import cv2
from PIL import Image
import traceback

from ThemesManager import ThemesManager
from MsgDialog import MsgDialog
from TopBar import TopBar
from Translator import Translator
from Card import Card
from ScaleManager import ScaleManager
from SettingsManager import SettingsManager

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scale_manager = ScaleManager()
        self.settings_manager = SettingsManager()

        self.current_language = self.settings_manager.get_language()
        self.translator = Translator(language=self.current_language, window=self)

        saved_theme = self.settings_manager.get_theme()
        self.theme_manager = ThemesManager(self, theme=saved_theme)

        self.selected_file = None
        self.selected_files = []
        self.selected_directory = None

        self.predict_enabled = False
        self.classifier = BrainTumorClassifier(CHECKPOINT_PATH)

        self.last_results = None
        self.result_type = None
        self.sorted_results = None

        # Window properties
        self.setWindowTitle("Neuron Desktop App")
        self.setMinimumSize(
            QSize(
                self.scale_manager.scale_value(1450),
                self.scale_manager.scale_value(840),
            )
        )

        self.setAttribute(Qt.WA_StyledBackground, True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar
        self.top_bar = TopBar(scale_manager=self.scale_manager, theme=saved_theme)
        self.top_bar.setContentsMargins(0, 0, 0, 50)

        lang_index = 0 if self.current_language == "EN" else 1
        self.top_bar.combobox_lang.setCurrentIndex(lang_index)

        self.top_bar.language_changed.connect(self.change_language)
        self.top_bar.theme_changed.connect(self.change_theme)

        # Main card
        self.card = Card(scale_manager=self.scale_manager, parent=self)
        self.card.sort_by.addItems(
            [
                self.get_text("sort_default"),
                self.get_text("sort_filename_az"),
                self.get_text("sort_filename_za"),
                self.get_text("sort_class_az"),
                self.get_text("sort_class_za"),
                self.get_text("sort_prob_asc"),
                self.get_text("sort_prob_desc"),
            ]
        )

        self.card.file_button.clicked.connect(self.open_file)
        self.card.dir_button.clicked.connect(self.open_directory)
        self.card.clear_button.clicked.connect(self.clear_selection)
        self.card.predict_button.clicked.connect(self.predict)
        self.card.sort_by.currentIndexChanged.connect(self.sort_results)

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

        self.theme_manager.apply_theme(theme=self.theme_manager.current_theme)
        self.translator.apply()

        saved_state = self.settings_manager.get_window_state()
        if saved_state == "maximized":
            self.showMaximized()
        else:
            saved_size = self.settings_manager.get_window_size()
            if saved_size:
                self.resize(saved_size)

            saved_position = self.settings_manager.get_window_position()
            if saved_position:
                self.move(saved_position)

        self.setCentralWidget(central_widget)

    def open_file(self):
        """
        Opens a file dialog for selecting one or more JPG images.
        """
        # Get user's 'Pictures' path
        pictures_path = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        window_title = self.get_text("open_file")

        # Fetch selected file(s) names
        filenames, _ = QFileDialog.getOpenFileNames(
            self, window_title, pictures_path, "JPG files (*.jpg *.jpeg)"
        )

        if not filenames:
            return

        # Turn the preview on
        self.card.preview_label.setVisible(False)
        self.card.preview_container.setVisible(True)

        # Wipe data just in case
        self.clear_thumbnails()

        if len(filenames) == 1:
            # User selected single file
            self.selected_file = filenames[0]
            self.selected_files = []

            file_name = os.path.basename(filenames[0])
            self.card.file_name_label.setText(
                f"{self.get_text("selected")}: {file_name}"
            )

            # Display thumbnail
            self.add_thumbnail(filenames[0])

        else:
            # User selected multiple files
            self.selected_file = None
            self.selected_files = filenames

            self.card.file_name_label.setText(
                f"{self.get_text("selected")}: {len(filenames)} {self.get_text('images')}"
            )

            # Display up to 3 thumbnails
            for filepath in filenames[:3]:
                self.add_thumbnail(filepath)

            if len(filenames) > 3:
                # Add more thumbnail
                more_label = QLabel(f"+{len(filenames) - 3}")
                more_label.setStyleSheet(
                    """
                    background-color: rgba(148, 211, 255, .3);
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    """
                )
                more_label.setAlignment(Qt.AlignCenter)
                more_label.setFixedSize(
                    self.get_preview_size(), self.get_preview_size()
                )

                # Add as the last element
                self.card.thumbnails_layout.addWidget(more_label)

        # Enable predict button
        self.predict_enabled = True
        self.card.predict_button.setEnabled(self.predict_enabled)

        # Enable clear button
        self.card.clear_button.setVisible(True)
        self.card.clear_button.setEnabled(True)

    def open_directory(self):
        window_title = (
            "Select Folder" if self.current_language == "EN" else "Wybierz folder"
        )
        dirname = QFileDialog.getExistingDirectory(self, window_title)

        if not dirname:
            return

        jpg_files = []
        if os.path.exists(dirname) and os.path.isdir(dirname):
            for filename in os.listdir(dirname):
                if filename.lower().endswith((".jpg", ".jpeg")):
                    filepath = os.path.join(dirname, filename)
                    if os.path.isfile(filepath):
                        jpg_files.append(filepath)

        self.card.preview_label.setVisible(False)
        self.card.preview_container.setVisible(True)
        self.clear_thumbnails()

        if jpg_files:
            self.selected_file = None
            self.selected_files = jpg_files
            self.selected_directory = dirname

            self.card.preview_label.setVisible(False)
            self.card.preview_container.setVisible(True)

            self.card.file_name_label.setText(
                self.get_text(
                    "selected_images",
                    count=len(jpg_files),
                    folder=os.path.basename(dirname),
                )
            )

            self.clear_thumbnails()
            self.show_directory_preview(jpg_files)

            self.card.clear_button.setVisible(True)
            self.card.clear_button.setEnabled(True)

            self.predict_enabled = True
            self.card.predict_button.setEnabled(self.predict_enabled)
        else:
            self.selected_files = []
            self.selected_directory = None

            self.card.file_name_label.setText(
                {self.get_text("no_jpg", folder=os.path.basename(dirname))}
            )
            self.predict_enabled = False
            self.card.predict_button.setEnabled(self.predict_enabled)
            self.card.clear_button.setVisible(False)
            self.card.clear_thumbnails()

    def predict(self):
        """
        Runs prediction for uploaded data.
        """
        if not self.predict_enabled:
            return

        self.card.predict_button.setText(self.get_text("thinking"))
        self.card.clear_button.setEnabled(False)

        # Refresh app before long processing operation
        QApplication.processEvents()
        print(f"selected_file: {self.selected_file}")
        print(f"selected_files: {self.selected_files}")
        try:
            if self.selected_file:
                res = self.classifier.predict(self.selected_file)
                res["filepath"] = self.selected_file
                self.show_single_res(res)
                self.result_type = "single"

            elif self.selected_files:
                res = self.classifier.predict_batch(self.selected_files)
                self.show_batch_res(res)
                self.result_type = "batch"
            self.last_results = res
            self.card.export_button.setEnabled(True)

        except Exception as e:
            title = (
                "Execution failed"
                if self.current_language == "EN"
                else "Wykonanie nie powiodło się"
            )
            error_msg = traceback.format_exc()
            MsgDialog(parent=self, title=title, msg=error_msg, type=QMessageBox.Critical)
            print(f"Prediction error: {e}")

        finally:
            label = "Predict" if self.current_language == "EN" else "Uruchom"
            self.card.sort_by.setCurrentIndex(0)
            self.card.predict_button.setText(label)
            self.card.predict_button.setEnabled(True)
            self.card.clear_button.setEnabled(True)

    def refresh_results(self):
        if self.last_results is None:
            return
        print(f"refreshing results... Result type: {self.result_type}")
        if self.result_type == "single":
            self.show_single_res(self.last_results)
        elif self.result_type == "batch":
            self.show_batch_res(self.last_results)

    def show_single_res(self, res):
        """
        Display prediction for one image.
        """
        self.clear_results()

        card = self.create_res_card(
            filename=os.path.basename(res["filepath"]),
            filepath=self.selected_file,
            pred=res["class_name"],
            confidence=res["probability"],
        )
        self.card.results_layout.addWidget(card)
        self.card.results_layout.addStretch()

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
                confidence=result["probability"],
            )
            self.card.results_layout.addWidget(card)

        self.card.results_layout.addStretch()

    def change_theme(self, theme):
        # Save current theme setting
        self.settings_manager.set_theme(theme=theme)

        # Apply UI theme
        self.theme_manager.apply_theme(theme)

        # Refresh results
        self.refresh_results()

    def clear_selection(self):
        # Clear chosen files
        self.selected_file = None
        self.selected_files = []
        self.selected_directory = None
        self.sorted_results = None

        self.card.preview_label.setVisible(True)
        self.card.preview_container.setVisible(False)

        self.card.file_name_label.setText("")
        self.clear_thumbnails()

        self.predict_enabled = False
        self.card.predict_button.setEnabled(self.predict_enabled)

        self.card.clear_button.setVisible(True)
        self.card.clear_button.setEnabled(False)

        self.card.sort_by.setCurrentIndex(0)

        self.clear_results()
        self.last_results = None
        self.result_type = None
        self.sort_results = None
        print("Selection cleared.")

    def get_preview_size(self):
        # Get 15% of current window size
        window_height = self.height()
        preview_size = int(window_height * 0.15)
        print(f"preview size: {preview_size}\nreturn:{max(80, min(preview_size, 150))}")

        # Return value between 80 and 150
        return max(80, min(preview_size, 150))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Scale thumbnails
        self.update_thumbnails_size()
        # Show confidence bars for larger windows
        self.update_confidence_bar_visibility()

    def update_thumbnails_size(self):
        preview_size = self.get_preview_size()

        for i in range(self.card.thumbnails_layout.count()):
            widget = self.card.thumbnails_layout.itemAt(i).widget()
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
                f"""
                background-color: rgba(148, 211, 255, .3);
                border-radius: 10px;
                font-size: {self.scale_manager.scale_font(16)}px;
                font-weight: bold;
            """
            )
            more_label.setAlignment(Qt.AlignCenter)
            more_label.setFixedSize(self.get_preview_size(), self.get_preview_size())
            more_label.setObjectName("more_label")
            self.card.thumbnails_layout.addWidget(more_label)

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

        self.card.thumbnails_layout.addWidget(thumbnail)

    def clear_thumbnails(self):
        while self.card.thumbnails_layout.count():
            item = self.card.thumbnails_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.clear_results()

    def create_res_card(self, filepath, filename, pred, confidence):
        """
        Create colorful result card for the pred.
        """
        colors = {
            "Light": {
                "glioma_tumor": "#DA5F62",
                "meningioma_tumor": "#F0B880",
                "no_tumor": "#93F080",
                "pituitary_tumor": "#F0F47A",
                "text": "black",
            },
            "Dark": {
                "glioma_tumor": "#982527",
                "meningioma_tumor": "#AC6723",
                "no_tumor": "#519A47",
                "pituitary_tumor": "#A6A637",
                "text": "#FFFAF2",
            },
        }

        current_theme = self.theme_manager.current_theme
        card_color = colors[current_theme][pred]

        card = QWidget()
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet(
            f"""
            QWidget {{
                background-color: {card_color};
                border-radius: 15px;
                font-size: {self.scale_manager.scale_font(16)}px;
            }}
            """
        )
        card.setFixedHeight(self.scale_manager.scale_value(60))

        layout = QHBoxLayout(card)
        layout.setContentsMargins(
            self.scale_manager.scale_value(10),
            self.scale_manager.scale_value(5),
            self.scale_manager.scale_value(10),
            self.scale_manager.scale_value(5),
        )
        layout.setSpacing(self.scale_manager.scale_value(10))

        name_label = QLabel(filename)
        name_label.setStyleSheet(f"background-color: transparent; border: none;")
        name_label.setFixedWidth(self.scale_manager.scale_value(120))
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        class_label = QLabel(self.get_text(pred))
        class_label.setStyleSheet(
            f"background-color: transparent; border: none; font-weight: bold;"
        )
        class_label.setFixedWidth(self.scale_manager.scale_value(160))
        class_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Confidence bar
        confidence_bar = QProgressBar(card)
        confidence_bar.setFixedSize(
            self.scale_manager.scale_value(180), self.scale_manager.scale_value(15)
        )
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
        confidence_bar.setVisible(self.width() >= self.scale_manager.scale_value(1600))
        print(
            f"width during creating res card: {self.width()}\nscaled value: {self.scale_manager.scale_value(1600)}"
        )

        conf_label = QLabel(f"{confidence*100:.2f}% {self.get_text("probability")}")
        conf_label.setStyleSheet(f"background-color: transparent; border: none;")
        conf_label.setFixedWidth(self.scale_manager.scale_value(280))
        conf_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        details_button = QPushButton("🔍")
        details_button.setFixedSize(
            self.scale_manager.scale_value(40), self.scale_manager.scale_value(40)
        )
        details_button.setCursor(Qt.PointingHandCursor)
        hint = (
            "Show GradCAM visualization"
            if self.current_language == "EN"
            else "Pokaż mapę ciepła GradCAM"
        )
        details_button.setToolTip(hint)
        details_button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-size: {self.scale_manager.scale_font(24)}px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 15px;
            }}
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
        show_bars = self.width() > self.scale_manager.scale_value(1600)

        for i in range(self.card.results_layout.count()):
            item = self.card.results_layout.itemAt(i)
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
                title = (
                    "Image loading failed"
                    if self.current_language == "EN"
                    else "Załadowanie obrazu nie powiodło się"
                )
                content = (
                    "Could not load the image"
                    if self.current_language == "EN"
                    else "Błąd podczas ładowania obrazu"
                )
                error_msg = traceback.format_exc()
                MsgDialog(
                    parent=self,
                    title=title,
                    msg=lambda f=filepath: f"{content}: {f}\n{error_msg}",
                    type=QMessageBox.Critical
                )
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
            gradcam_dialog.setWindowTitle(
                f"{self.get_text("gradcam_title")} {os.path.basename(filepath)}"
            )
            gradcam_dialog.setMinimumSize(600, 300)

            gradcam_layout = QVBoxLayout(gradcam_dialog)
            images_layout = QHBoxLayout()

            original_container = QVBoxLayout()
            original_label = QLabel(
                f"{self.get_text("original")}\n{os.path.basename(filepath)}"
            )
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
            heatmap_label = QLabel(self.get_text("heatmap"))
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
            superimposed_label = QLabel(self.get_text("overlay"))
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
                f"{self.get_text("prediction")}: {self.get_text(self.classifier.classes[res["class_index"]])} ({res["probability"]*100:.2f}%)"
            )
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setStyleSheet(
                f"font-size: {self.scale_manager.scale_font(18)}px; margin-top: 10px;"
            )

            gradcam_layout.addLayout(images_layout)
            gradcam_layout.addWidget(info_label)

            self.setCursor(Qt.ArrowCursor)
            gradcam_dialog.exec()

        except Exception as e:
            title = (
                "Visualization error has occured."
                if self.current_language == "EN"
                else "Wystąpił błąd wizualizacji."
            )
            error_msg = traceback.format_exc()
            MsgDialog(parent=self, title=title, msg=error_msg, type=QMessageBox.Critical)
            print(f"GradCAM error: {e}")
            self.setCursor(Qt.ArrowCursor)

    def rgb_to_pixmap(self, rgb_img):
        height, width, channel = rgb_img.shape
        bytes_per_line = width * channel

        qimg = QImage(rgb_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg.copy())

    def change_language(self, language):
        print(f"change_language called with: {language}")
        self.current_language = language

        # Save current setting
        self.settings_manager.set_language(language=language)

        # Translate the UI
        self.translator = Translator(window=self, language=self.current_language)
        self.translator.apply()

        # Refresh UI elements
        self.refresh_results()
        self.refresh_sort_combobox()

    def sort_results(self, index):
        if self.last_results is None or self.result_type == "single":
            return

        res = self.last_results.copy()
        if index == 0:
            res = self.last_results.copy()
        elif index == 1:
            # Filename A-Z
            res.sort(key=lambda x: os.path.basename(x["filepath"]).lower())
        elif index == 2:
            # Filename Z-A
            res.sort(
                key=lambda x: os.path.basename(x["filepath"]).lower(), reverse=True
            )
        elif index == 3:
            # Classname A-Z
            res.sort(
                key=lambda x: os.path.basename(self.get_text(x["class_name"])).lower()
            )
        elif index == 4:
            # Classname Z-A
            res.sort(
                key=lambda x: os.path.basename(self.get_text(x["class_name"])).lower(),
                reverse=True,
            )
        elif index == 5:
            # Confidence ASC
            res.sort(key=lambda x: x["probability"])
        elif index == 6:
            # Confidence DESC
            res.sort(key=lambda x: x["probability"], reverse=True)

        self.sorted_results = res
        self.rebuild_result_card()

    def rebuild_result_card(self):
        self.clear_results()

        if self.sorted_results is None:
            return

        for res in self.sorted_results:
            card = self.create_res_card(
                filepath=res["filepath"],
                filename=os.path.basename(res["filepath"]),
                pred=res["class_name"],
                confidence=res["probability"],
            )
            self.card.results_layout.addWidget(card)

        self.card.results_layout.addStretch()
        self.update_confidence_bar_visibility()

    def refresh_sort_combobox(self):
        idx = self.card.sort_by.currentIndex()

        self.card.sort_by.blockSignals(True)
        self.card.sort_by.clear()
        self.card.sort_by.addItems(
            [
                self.get_text("sort_default"),
                self.get_text("sort_filename_az"),
                self.get_text("sort_filename_za"),
                self.get_text("sort_class_az"),
                self.get_text("sort_class_za"),
                self.get_text("sort_prob_asc"),
                self.get_text("sort_prob_desc"),
            ]
        )

        self.card.sort_by.setCurrentIndex(idx)
        self.card.sort_by.blockSignals(False)

    def get_text(self, key, **kwargs):
        return self.translator.get_text(key, **kwargs)

    def clear_results(self):
        """
        Clears results card.
        """
        self.card.export_button.setEnabled(False)
        while self.card.results_layout.count():
            item = self.card.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                pass

    def closeEvent(self, event):
        """Save window size and position before closing the app"""
        if self.isMaximized():
            self.settings_manager.set_window_state("maximized")
        else:
            self.settings_manager.set_window_state("normal")
            self.settings_manager.set_window_size(self.size())
            self.settings_manager.set_window_position(self.pos())

        event.accept()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
