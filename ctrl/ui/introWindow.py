
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from .mainWindow import MainWindow
from ..macro import Macro

form_class = uic.loadUiType("view/introWindow.ui")[0]


class IntroWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.set_info()
        self.progressBar.hide()
        self.LoginButton.clicked.connect(self.login)

    def set_info(self):
        self.selectBrowser.addItem("Chrome으로 실행 (추천)")
        self.selectBrowser.addItem("IE9으로 실행 (지원예정)")

    def login(self):
        pbar = self.progressBar
        pbar.show()
        pbar.setValue(0)
        browser = self.selectBrowser.currentIndex()
        uid = self.uid.text()
        pwd = self.pwd.text()
        macro = Macro(browser)
        is_success = macro.login(uid, pwd, self.progressBar)
        if is_success == True:
            mainWindow = MainWindow(macro)
            mainWindow.setupUi(self.window)
            self.window.show()
            self.close()
        else:
            macro.driver.quit()
            del macro
            self.alert('warning', '경고', '로그인에 실패했습니다.')

    def alert(self, status, title, message):
        action = {
            'warning': QMessageBox.warning,
            'informaion': QMessageBox.information,
            'critical': QMessageBox.critical,
            'about': QMessageBox.about
        }
        return action[status](self.centralwidget, title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = IntroWindow()
    myWindow.show()
    app.exec_()
