from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QWidget,
    QStyledItemDelegate,
)
from PyQt5.QtCore import Qt, pyqtSignal


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, height=30):
        super().__init__()
        self.item_height = height

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(self.item_height)
        return size


class TopBar(QWidget):
    theme_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)

    def __init__(self, scale_manager, theme="Light"):
        super().__init__()

        self.theme = theme
        self.scale_manager = scale_manager

        self.small_font = scale_manager.scale_font(16)
        self.title_font = scale_manager.scale_font(44)
        self.setStyleSheet(f"font-size: {self.small_font}px;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            self.scale_manager.scale_value(20),
            self.scale_manager.scale_value(10),
            self.scale_manager.scale_value(20),
            self.scale_manager.scale_value(10),
        )
        main_layout.setSpacing(self.scale_manager.scale_value(5))

        top_row = QHBoxLayout()
        top_row.addStretch()

        self.combobox_lang = QComboBox()
        self.combobox_lang.setItemDelegate(
            ItemDelegate(height=scale_manager.scale_value(40))
        )
        self.combobox_lang.addItems(["EN", "PL"])
        self.combobox_lang.setFixedSize(
            self.scale_manager.scale_value(90), self.scale_manager.scale_value(45)
        )
        self.combobox_lang.setCursor(Qt.PointingHandCursor)
        self.combobox_lang.view().setCursor(Qt.PointingHandCursor)
        self.combobox_lang.currentTextChanged.connect(self.change_lang)

        self.light_theme = QPushButton("Light 🔆")
        self.light_theme.setCursor(Qt.PointingHandCursor)
        self.light_theme.clicked.connect(self.set_light_theme)

        self.dark_theme = QPushButton("🌙 Dark")
        self.dark_theme.setCursor(Qt.PointingHandCursor)
        self.dark_theme.clicked.connect(self.set_dark_theme)

        for button in [self.light_theme, self.dark_theme]:
            button.setFixedSize(
                self.scale_manager.scale_value(140), self.scale_manager.scale_value(40)
            )

        top_row.addWidget(self.combobox_lang)
        top_row.addSpacing(self.scale_manager.scale_value(15))
        top_row.addWidget(self.dark_theme)
        top_row.addWidget(self.light_theme)

        logo_row = QHBoxLayout()
        logo_row.addStretch()

        self.app_name = QLabel("Neuron")
        self.app_name.setStyleSheet(
            f"""
            font-size: {self.title_font}px;
            font-weight: 300;
            """
        )

        logo_row.addWidget(self.app_name)
        logo_row.addStretch()

        main_layout.addLayout(top_row)
        main_layout.addLayout(logo_row)

        self.update_theme()

    def set_light_theme(self):
        self.theme = "Light"
        self.update_theme()
        self.theme_changed.emit("Light")

    def set_dark_theme(self):
        self.theme = "Dark"
        self.update_theme()
        self.theme_changed.emit("Dark")

    def update_theme(self):
        border_radius = self.scale_manager.scale_value(10)
        if self.theme.lower() == "light":
            self.light_theme.setChecked(True)
            self.light_theme.setEnabled(False)
            self.light_theme.setStyleSheet(
                f"""
                QPushButton {{
                    border-radius: {border_radius}px;
                    padding: 5px 10px;
                    background-color: white;
                    color: black;
                }}
                """
            )

            self.dark_theme.setChecked(False)
            self.dark_theme.setEnabled(True)
            self.dark_theme.setStyleSheet(
                f"""
                QPushButton {{
                    border-radius: {border_radius}px;
                    padding: 5px 10px;
                    background: transparent;
                    color: black;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.5);
                }}
                """
            )

            self.combobox_lang.setStyleSheet(
                f"""
            QComboBox {{
                font-weight: Normal;
                border: 1px solid #ccc;
                padding: 5px 10px;
                background: white;
                font-size: {self.small_font}px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: black;
                selection-background-color: rgba(148, 211, 255, .72);
                selection-color: black;
                font-size: {self.small_font}px;
            }}
            """
            )

        else:
            self.dark_theme.setChecked(True)
            self.dark_theme.setEnabled(False)
            self.dark_theme.setStyleSheet(
                f"""
                QPushButton {{
                    border-radius: {border_radius}px;
                    padding: 5px 10px;
                    background-color: #376281;
                    color: #FFFAF2;
                }}
                """
            )

            self.light_theme.setChecked(False)
            self.light_theme.setEnabled(True)
            self.light_theme.setStyleSheet(
                f"""
                QPushButton {{
                    border-radius: {border_radius}px;
                    padding: 5px 10px;
                    background: transparent;
                    color: #FFFAF2;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.2);
                }}
                """
            )

            self.combobox_lang.setStyleSheet(
                f"""
            QComboBox {{
                font-weight: Normal;
                border: 1px solid #ccc;
                padding: 5px 10px;
                background: #376281;
                color: #FFFAF2;
                font-size: {self.small_font}px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #1B2037;
                color: #FFFAF2;
                selection-background-color: #376281;
                selection-color: #FFFAF2;
                font-size: {self.small_font}px;
            }}
            """
            )

    def change_lang(self, current_item):
        if current_item == "EN":
            self.dark_theme.setText("🌙 Dark")
            self.light_theme.setText("Light 🔆")
        elif current_item == "PL":
            self.dark_theme.setText("🌙 Ciemny")
            self.light_theme.setText("Jasny 🔆")

        self.language_changed.emit(current_item)
