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
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(30)
        return size


class TopBar(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self, lang="EN", theme="Light"):
        super().__init__()

        self.theme = theme
        self.setStyleSheet("font-size: 12px;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(5)

        top_row = QHBoxLayout()
        top_row.addStretch()

        self.combobox_lang = QComboBox()
        self.combobox_lang.setItemDelegate(ItemDelegate())
        self.combobox_lang.addItems(["EN", "PL"])
        self.combobox_lang.setMinimumSize(40, 30)
        self.combobox_lang.setCursor(Qt.PointingHandCursor)
        self.combobox_lang.view().setCursor(Qt.PointingHandCursor)

        self.light_theme = QPushButton("Light 🔆")
        self.light_theme.setCursor(Qt.PointingHandCursor)
        self.light_theme.clicked.connect(self.set_light_theme)

        self.dark_theme = QPushButton("🌙 Dark")
        self.dark_theme.setCursor(Qt.PointingHandCursor)
        self.dark_theme.clicked.connect(self.set_dark_theme)

        for button in [self.light_theme, self.dark_theme]:
            button.setMinimumSize(50, 30)

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

        self.update_theme()

    def set_light_theme(self):
        self.theme = "light"
        self.update_theme()
        self.theme_changed.emit("light")

    def set_dark_theme(self):
        self.theme = "dark"
        self.update_theme()
        self.theme_changed.emit("dark")

    def update_theme(self):
        if self.theme.lower() == "light":
            self.light_theme.setChecked(True)
            self.light_theme.setEnabled(False)
            self.light_theme.setStyleSheet(
                """
                QPushButton {
                    border-radius: 10px;
                    padding: 5px 10px;
                    background-color: white;
                    color: black;
                }
                """
            )

            self.dark_theme.setChecked(False)
            self.dark_theme.setEnabled(True)
            self.dark_theme.setStyleSheet(
                """
                QPushButton {
                    border-radius: 10px;
                    padding: 5px 10px;
                    background: transparent;
                    color: black;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.5);
                }
                """
            )

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

        else:
            self.dark_theme.setChecked(True)
            self.dark_theme.setEnabled(False)
            self.dark_theme.setStyleSheet(
                """
                QPushButton {
                    border-radius: 10px;
                    padding: 5px 10px;
                    background-color: #376281;
                    color: #FFFAF2;
                }
                """
            )

            self.light_theme.setChecked(False)
            self.light_theme.setEnabled(True)
            self.light_theme.setStyleSheet(
                """
                QPushButton {
                    border-radius: 10px;
                    padding: 5px 10px;
                    background: transparent;
                    color: #FFFAF2;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
                """
            )

            self.combobox_lang.setStyleSheet(
                """
            QComboBox {
                font-weight: Normal;
                border: 1px solid #ccc;
                padding: 5px 10px;
                background: #376281;
                color: #FFFAF2;
            }
            QComboBox QAbstractItemView {
                background-color: #1B2037;
                color: #FFFAF2;
                selection-background-color: #376281;
                selection-color: #FFFAF2;
            }
            """
            )
