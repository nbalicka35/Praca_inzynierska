import os
from PyQt5.QtWidgets import QWidget, QScrollArea, QFileDialog, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QStandardPaths

class Card(QWidget):
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 45
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.window = parent
        self.create_card()
        
    def create_card(self):
        self.setObjectName("card")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.card_layout = QHBoxLayout(self)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)
        
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
        self.step1_label = QLabel("Step 1")
        self.step1_desc = QLabel("Select JPG file(s) or directory")
        
        buttons_layout = QHBoxLayout()
        
        self.file_button = QPushButton("Choose file(s)")
        self.file_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.file_button.setCursor(Qt.PointingHandCursor)

        self.dir_button = QPushButton("Choose directory")
        self.dir_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.dir_button.setCursor(Qt.PointingHandCursor)

        buttons_layout.addWidget(self.file_button)
        buttons_layout.addWidget(self.dir_button)
        buttons_layout.addStretch()
        
        # Image(s) preview section
        self.preview_label = QLabel("Preview of selected image(s) will appear below")

        self.preview_container = QWidget()
        self.preview_container.setAttribute(Qt.WA_StyledBackground, True)
        self.preview_container.setVisible(False)

        preview_container_layout = QVBoxLayout(self.preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)
        preview_container_layout.setSpacing(10)

        self.file_name_label = QLabel("")
        
        image_row = QHBoxLayout()
        image_row.setAlignment(Qt.AlignLeft)
        image_row.setSpacing(10)

        self.thumbnails_container = QWidget()
        self.thumbnails_layout = QHBoxLayout(self.thumbnails_container)
        self.thumbnails_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnails_layout.setSpacing(10)
        self.thumbnails_layout.setAlignment(Qt.AlignLeft)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setEnabled(False)

        image_row.addWidget(self.thumbnails_container)
        image_row.addSpacing(20)
        image_row.addWidget(self.clear_button, alignment=Qt.AlignBottom)
        image_row.addStretch()

        preview_container_layout.addWidget(self.file_name_label)
        preview_container_layout.addLayout(image_row)

        # Step 2
        self.step2_label = QLabel("Step 2")
        self.step2_desc = QLabel("Examine photo(s)")

        # Predict button
        predict_layout = QHBoxLayout()
        
        self.predict_button = QPushButton("Predict")
        self.predict_button.setEnabled(False)
        self.predict_button.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.predict_button.setCursor(Qt.PointingHandCursor)
        
        predict_layout.addWidget(self.predict_button)
        predict_layout.addStretch()

        # Disclaimer
        disclaimer_layout = QHBoxLayout()
        disclaimer_layout.setAlignment(Qt.AlignLeft)
        disclaimer_layout.setSpacing(5)

        self.disclaimer_icon = QLabel("⚠️")
        self.disclaimer_icon.setAlignment(Qt.AlignTop)

        self.disclaimer_text = QLabel(
            "Please note that Neuron is a software designed to support physicians and radiologists, and can make mistakes.\n"
            "Always examine patients and make a decision based on the knowledge of yours."
        )
        self.disclaimer_text.setAlignment(Qt.AlignLeft)

        disclaimer_layout.addWidget(self.disclaimer_icon)
        disclaimer_layout.addWidget(self.disclaimer_text)
        disclaimer_layout.addStretch()

        self.left_column.addWidget(self.step1_label)
        self.left_column.addWidget(self.step1_desc)
        self.left_column.addLayout(buttons_layout)
        self.left_column.addWidget(self.preview_label)
        self.left_column.addWidget(self.preview_container)
        self.left_column.addSpacing(20)
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
        self.step3_label = QLabel("Step 3")
        self.step3_desc = QLabel("Check the result for the photo(s) below")

        sort_layout = QHBoxLayout()
        sort_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # Sort options
        self.sort_label = QLabel("Sort by:")
        
        self.sort_by = QComboBox()
        self.sort_by.setFixedSize(200, 40)
        self.sort_by.setCursor(Qt.PointingHandCursor)
        self.sort_by.view().setCursor(Qt.PointingHandCursor)
        
        sort_layout.addWidget(self.sort_label)
        sort_layout.addWidget(self.sort_by)
        
        # Result(s) panel
        self.results_card = QScrollArea()
        self.results_card.setObjectName("results_card")
        self.results_card.setWidgetResizable(True)
        self.results_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.results_card.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_card.setMinimumHeight(300)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(15, 15, 15, 15)
        self.results_layout.setSpacing(10)
        self.results_layout.setAlignment(Qt.AlignTop)

        self.results_card.setWidget(self.results_container)

        self.right_column.addWidget(self.step3_label)
        self.right_column.addWidget(self.step3_desc)
        self.right_column.addLayout(sort_layout)
        self.right_column.addWidget(self.results_card, 1)
    