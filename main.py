#!/usr/bin/python
"reservation app proto type"
import sys
from PyQt5.QtWidgets import QApplication
from ctrl import ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = ui.IntroWindow()
    myWindow.show()
    app.exec()
