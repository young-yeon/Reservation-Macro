"인트로 화면 (~로그인)"
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic

from .main_window import MainWindow
from ..macro import Macro

form_class = uic.loadUiType("view/introWindow.ui")[0]


class IntroWindow(QMainWindow, form_class):
    "인트로 화면(UI: introWindow.ui)"
    def __init__(self, stack, parent=None):
        super(IntroWindow, self).__init__(parent)
        self.setupUi(self)
        self.set_info()
        self.progressBar.hide()
        self.LoginButton.clicked.connect(self.login)
        self.stack = stack

    def set_info(self):
        "브라우저 선택지 제공"
        self.selectBrowser.addItem("Chrome으로 실행 (추천)")
        self.selectBrowser.addItem("IE9으로 실행 (지원예정)")

    def login(self):
        "로그인 정보 받아서 macro에 넘겨주기"
        pbar = self.progressBar
        pbar.show()
        pbar.setValue(0)
        browser = self.selectBrowser.currentIndex()
        uid = self.uid.text()
        pwd = self.pwd.text()
        macro = Macro(browser)
        status = macro.login(uid, pwd, self.progressBar)
        if status.success is True:
            main_window = MainWindow(macro, self.stack)
            self.stack.addWidget(main_window)
            self.stack.setCurrentIndex(1)
        else:
            if status.code == -1:
                self.alert('information', '정보', '현재 지원되지 않는 브라우저입니다.')
            elif status.code == -2:
                macro.driver.quit()
                del macro
                self.alert('warning', '경고', '로그인에 실패했습니다.')
            elif status.code == -3:
                macro.driver.quit()
                del macro
                self.alert('warning', '경고', '인터넷 연결에 실패했습니다.')

    def alert(self, status, title, message):
        "메시지 얼럴트"
        action = {
            'warning': QMessageBox.warning,
            'information': QMessageBox.information,
            'critical': QMessageBox.critical,
            'about': QMessageBox.about
        }
        return action[status](self.centralwidget, title, message)
