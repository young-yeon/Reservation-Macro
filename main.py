import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from ctrl import ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = ui.IntroWindow()
    myWindow.show()
    app.exec()