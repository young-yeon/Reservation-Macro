#!/usr/bin/python
"reservation app proto type"
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ctrl import ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    intro = ui.IntroWindow(stack)
    stack.addWidget(intro)
    stack.show()
    sys.exit(app.exec())
