#!/usr/bin/python
"reservation app proto type"
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from ctrl import ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('남여주 예약 도구')
    app.setWindowIcon(QIcon('view/golf-ball.png'))
    app.setApplicationVersion('1.1')
    stack = QStackedWidget()
    intro = ui.IntroWindow(stack)
    stack.addWidget(intro)
    stack.show()
    sys.exit(app.exec())
