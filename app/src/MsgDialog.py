from PyQt5.QtWidgets import QMessageBox


class MsgDialog(QMessageBox):
    """
    Universal dialogs
    """
    
    def __init__(self, parent, title, msg, type=QMessageBox.Information):
        super().__init__(parent)

        self.setIcon(type)
        self.setWindowTitle(title)
        self.setText(msg)
        self.setStandardButtons(QMessageBox.Ok)
        self.exec_()
