
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from datetime import date


form_class = uic.loadUiType("view/mainWindow.ui")[0]


class MainWindow(QMainWindow, form_class):
    def __init__(self, Macro):
        self.macro = Macro
        super().__init__()
        self.setupUi(self)
        self.progressBar.hide()
        self.set_today()
    
    def set_today(self):
        today = date.today()
        self.targetDate.setDate(today)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow(0, 0, 0)
    myWindow.show()
    app.exec_()
