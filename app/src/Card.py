from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QComboBox,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from TopBar import ItemDelegate
from MsgDialog import MsgDialog

class Card(QWidget):

    def __init__(self, scale_manager, parent=None):
        super().__init__(parent)

        self.window = parent
        self.scale_manager = scale_manager
        self.BUTTON_WIDTH = self.scale_manager.scale_value(200)
        self.BUTTON_HEIGHT = self.scale_manager.scale_value(60)

        self.create_card()

    def create_card(self):
        self.setObjectName("card")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.card_layout = QHBoxLayout(self)
        self.card_layout.setContentsMargins(
            self.scale_manager.scale_value(40),
            self.scale_manager.scale_value(40),
            self.scale_manager.scale_value(40),
            self.scale_manager.scale_value(40),
        )
        self.card_layout.setSpacing(self.scale_manager.scale_value(20))

        self.create_left_column()
        self.create_right_column()

        # Add columns to the card
        self.card_layout.addLayout(self.left_column, 1)
        self.card_layout.addLayout(self.right_column, 1)

    def create_left_column(self):
        # Left column inside the card
        self.left_column = QVBoxLayout()
        self.left_column.setAlignment(Qt.AlignTop)

        # Step 1
        self.step1_label = QLabel()
        self.step1_desc = QLabel()

        buttons_layout = QHBoxLayout()

        self.file_button = QPushButton()
        self.file_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.file_button.setCursor(Qt.PointingHandCursor)

        self.dir_button = QPushButton()
        self.dir_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.dir_button.setCursor(Qt.PointingHandCursor)

        buttons_layout.addWidget(self.file_button)
        buttons_layout.addWidget(self.dir_button)
        buttons_layout.addStretch()

        # Image(s) preview section
        self.preview_label = QLabel()

        self.preview_container = QWidget()
        self.preview_container.setAttribute(Qt.WA_StyledBackground, True)
        self.preview_container.setVisible(False)

        preview_container_layout = QVBoxLayout(self.preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)
        preview_container_layout.setSpacing(self.scale_manager.scale_value(10))

        self.file_name_label = QLabel("")

        image_row = QHBoxLayout()
        image_row.setAlignment(Qt.AlignLeft)
        image_row.setSpacing(self.scale_manager.scale_value(10))

        self.thumbnails_container = QWidget()
        self.thumbnails_layout = QHBoxLayout(self.thumbnails_container)
        self.thumbnails_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnails_layout.setSpacing(self.scale_manager.scale_value(10))
        self.thumbnails_layout.setAlignment(Qt.AlignLeft)

        # Clear button
        self.clear_button = QPushButton()
        self.clear_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setEnabled(False)

        image_row.addWidget(self.thumbnails_container)
        image_row.addSpacing(self.scale_manager.scale_value(20))
        image_row.addWidget(self.clear_button, alignment=Qt.AlignBottom)
        image_row.addStretch()

        preview_container_layout.addWidget(self.file_name_label)
        preview_container_layout.addLayout(image_row)

        # Step 2
        self.step2_label = QLabel()
        self.step2_desc = QLabel()

        # Predict button
        predict_layout = QHBoxLayout()

        self.predict_button = QPushButton()
        self.predict_button.setEnabled(False)
        self.predict_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.predict_button.setCursor(Qt.PointingHandCursor)

        predict_layout.addWidget(self.predict_button)
        predict_layout.addStretch()

        # Disclaimer
        disclaimer_layout = QHBoxLayout()
        disclaimer_layout.setAlignment(Qt.AlignLeft)
        disclaimer_layout.setSpacing(self.scale_manager.scale_value(5))

        self.disclaimer_icon = QLabel("⚠️")
        self.disclaimer_icon.setAlignment(Qt.AlignTop)

        self.disclaimer_text = QLabel()
        self.disclaimer_text.setAlignment(Qt.AlignLeft)
        self.disclaimer_text.setOpenExternalLinks(False)
        self.disclaimer_text.setCursor(Qt.PointingHandCursor)
        self.disclaimer_text.linkActivated.connect(self.show_model_info)

        disclaimer_layout.addWidget(self.disclaimer_icon)
        disclaimer_layout.addWidget(self.disclaimer_text)
        disclaimer_layout.addStretch()

        self.left_column.addWidget(self.step1_label)
        self.left_column.addWidget(self.step1_desc)
        self.left_column.addLayout(buttons_layout)
        self.left_column.addWidget(self.preview_label)
        self.left_column.addWidget(self.preview_container)
        self.left_column.addSpacing(self.scale_manager.scale_value(20))
        self.left_column.addWidget(self.step2_label)
        self.left_column.addWidget(self.step2_desc)
        self.left_column.addLayout(predict_layout)
        self.left_column.addStretch()
        self.left_column.addLayout(disclaimer_layout)

    def create_right_column(self):
        # Right column inside the card
        self.right_column = QVBoxLayout()
        self.right_column.setAlignment(Qt.AlignTop)

        # Step 3
        self.step3_label = QLabel()
        self.step3_desc = QLabel()

        sort_layout = QHBoxLayout()
        sort_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.export_button = QPushButton()
        self.export_button.setCursor(Qt.PointingHandCursor)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_to_csv)

        # Sort options
        self.sort_label = QLabel()

        self.sort_by = QComboBox()
        self.sort_by.setItemDelegate(
            ItemDelegate(height=self.scale_manager.scale_value(40))
        )
        self.sort_by.setFixedSize(
            self.scale_manager.scale_value(200), self.scale_manager.scale_value(50)
        )
        self.sort_by.setCursor(Qt.PointingHandCursor)
        self.sort_by.view().setCursor(Qt.PointingHandCursor)

        sort_layout.addWidget(self.export_button)
        sort_layout.addStretch()
        sort_layout.addWidget(self.sort_label)
        sort_layout.addWidget(self.sort_by)

        # Result(s) panel
        self.results_card = QScrollArea()
        self.results_card.setObjectName("results_card")
        self.results_card.setWidgetResizable(True)
        self.results_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.results_card.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_card.setMinimumHeight(self.scale_manager.scale_value(300))

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(
            self.scale_manager.scale_value(15),
            self.scale_manager.scale_value(15),
            self.scale_manager.scale_value(15),
            self.scale_manager.scale_value(15),
        )
        self.results_layout.setSpacing(self.scale_manager.scale_value(10))
        self.results_layout.setAlignment(Qt.AlignTop)

        self.results_card.setWidget(self.results_container)

        self.right_column.addWidget(self.step3_label)
        self.right_column.addWidget(self.step3_desc)
        self.right_column.addLayout(sort_layout)
        self.right_column.addWidget(self.results_card, 1)

    def show_model_info(self):
        title = "More info" if self.window.current_language == "EN" else "Więcej informacji"
        msg_en = (
            "Classification model: ResNet-34\n\n"
            "Performance metrics:\n"
            "- Accuracy: X% — overall correct predictions\n"
            "- Precision: X% — reliability of positive predictions\n\n"
            "Important notes:\n"
            "The \"no tumor\" category had fewer training samples and were artificially increased, "
            "so predictions for healthy scans may be less reliable.\n\n"
            "Always verify results with clinical assessment."
        )
        
        msg_pl = (
            "Model klasyfikacji: ResNet-34\n\n"
            "Metryki wydajności:\n"
            "- Dokładność (accuracy): X% — odsetek poprawnych predykcji\n"
            "- Precyzja (precision): X% — wiarygodność pozytywnych wyników\n\n"
            "Ważne informacje:\n"
            "Kategoria \"brak guza\" miała mniej próbek treningowych, dlatego ich liczba została sztucznie zwiększona. "
            "Predykcje dla zdrowych skanów mogą być mniej wiarygodne.\n\n"
            "Zawsze weryfikuj wyniki z oceną kliniczną."
        )
        
        msg = msg_en if self.window.current_language == "EN" else msg_pl
        MsgDialog(parent=self.window, title=title, msg=msg, type=QMessageBox.Information)
    
    def export_to_csv(self):
        print("Export called!")
        
        self.window.export_to_csv()