from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QWidget,
)
from PyQt5.QtCore import Qt


class TopBar(QWidget):
    def __init__(self, lang="EN", theme="Light"):
        super().__init__()

        self.setStyleSheet("font-size: 12px;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(5)

        top_row = QHBoxLayout(self)
        top_row.addStretch()

        self.combobox_lang = QComboBox()
        self.combobox_lang.addItems(["EN", "PL"])
        self.combobox_lang.setMinimumSize(40, 30)
        self.combobox_lang.setStyleSheet(
            """
            QComboBox {
                font-weight: Normal;
                border: 1px solid #ccc;
                padding: 5px 10px;
                background: white;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: rgba(148, 211, 255, .72);
                selection-color: black;
            }
        """
        )

        self.light_theme = QPushButton("Light 🔆")
        self.dark_theme = QPushButton("🌙 Dark")

        for button in [self.light_theme, self.dark_theme]:
            button.setCheckable(True)
            button.setMinimumSize(50, 30)
            button.setStyleSheet(
                """
                QPushButton {
                    border-radius: 10px;
                    padding: 5px 10px;
                    background: transparent;
                }
                QPushButton:hover {
                    background: white;
                }
            """
            )

        top_row.addWidget(self.combobox_lang)
        top_row.addSpacing(15)
        top_row.addWidget(self.dark_theme)
        top_row.addWidget(self.light_theme)

        logo_row = QHBoxLayout()
        logo_row.addStretch()

        self.app_name = QLabel("Neuron")
        self.app_name.setStyleSheet(
            """
            font-size: 36px;
            font-weight: 300;
            """
        )

        logo_row.addWidget(self.app_name)
        logo_row.addStretch()

        main_layout.addLayout(top_row)
        main_layout.addLayout(logo_row)
