from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

form_class = uic.loadUiType("view/waitingWindow.ui")[0]

class WaitingWindow(QMainWindow, form_class):
    "대기 화면(UI: waitingWindow.ui)"
    def __init__(self, stack, parent=None):
        super(WaitingWindow, self).__init__(parent)
        self.setupUi(self)
        self.stack = stack
        