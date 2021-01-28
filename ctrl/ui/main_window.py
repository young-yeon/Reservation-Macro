"메인화면 (일정선택~)"
from datetime import date

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


form_class = uic.loadUiType("view/mainWindow.ui")[0]


class MainWindow(QMainWindow, form_class):
    "일정 조회하고 결정하는 화면(UI: mainWindow.ui)"
    def __init__(self, Macro):
        self.macro = Macro
        super().__init__()
        self.setupUi(self)
        self.progressBar.hide()
        self.set_today()

    def set_today(self):
        "오늘 날짜로 설정"
        today = date.today()
        self.targetDate.setMinimumDate(today)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(__import__('sys').argv)
    myWindow = MainWindow(0, 0, 0)
    myWindow.show()
    app.exec_()
    