from PyQt5.QtWidgets import QMessageBox


class ErrMsgDialog(QMessageBox):
    """
    Class for error dialogs
    """

    def __init__(self, parent, title, msg):
        super().__init__(parent)

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(title)
        self.setText(msg)
        self.setStandardButtons(QMessageBox.Ok)
        self.exec_()
