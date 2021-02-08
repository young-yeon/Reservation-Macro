"메인화면 (일정선택~)"
from datetime import date
import re

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QDateTime

from selenium.common.exceptions import NoAlertPresentException

from .time_parser import parser
from .waiting_window import WaitingWindow

form_class = uic.loadUiType("view/mainWindow.ui")[0]


class MainWindow(QMainWindow, form_class):
    "일정 조회하고 결정하는 화면(UI: mainWindow.ui)"

    def __init__(self, Macro, stack, parent=None):
        self.macro = Macro
        self.stack = stack
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.targetTime.hide()
        self.choice_2.hide()
        self.nextButton.hide()
        self.set_today()
        self.searchButton.clicked.connect(self.search_time)
        self.nextButton.clicked.connect(self.run)
        self.targetList.itemClicked.connect(self.load_resv)
        # 예약 가능 시간 리스트
        self.data = list()
        # 예약 예정 시간
        # ['연(yyyy)', '월(MM)', '일(dd)', '시(hh)', '분(mm)', '초(ss)']
        self.target_time = None

    def set_today(self):
        "오늘 날짜로 설정"
        today = date.today()
        self.targetDate.setMinimumDate(today)

    def search_time(self):
        "예약 가능 시간 검색"
        target = self.targetDate.date().toString("yyyyMMdd")
        self.macro.driver.get(
            "https://www.namyeoju.co.kr/Reservation/Reservation.aspx?SelectedDate="+target)
        self.targetList.clear()
        try:
            self.data = parser(self.macro.driver.page_source)
            for row in self.data:
                self.targetList.addItem(row[0])
            self.alert("information", "참고",
                       "그린피가 0원으로 표시될 경우 조금 뒤에 다시 조회해주세요.")
        except IndexError:
            self.alert("warning", "조회 실패", "예약 가능한 시간이 없습니다.")

    def load_resv(self):
        "예약 가능 시간 조회"
        current = self.targetList.currentRow()
        target = self.targetDate.date().toString("yyyyMMdd")
        self.macro.driver.get(
            "https://www.namyeoju.co.kr/Reservation/Reservation.aspx?SelectedDate="+target)
        try:
            self.macro.driver.execute_script(self.data[current][1])
            result = self.macro.driver.switch_to_alert()
            target_time = re.findall(r'\d+', result.text)
            if len(target_time) < 6:
                result.accept()
                raise IndexError
            self.target_time = list(map(int, target_time))
            result.accept()
        except (NoAlertPresentException, IndexError):
            self.macro.driver.set_window_size(1024, 768)
            self.target_time = None
        if self.target_time is not None:
            self.targetTime.show()
            self.choice_2.show()
            self.nextButton.show()
            qtime = QDateTime(self.target_time[0], self.target_time[1], self.target_time[2],
                              self.target_time[3], self.target_time[4], self.target_time[5])
            self.targetTime.setDateTime(qtime)

    def target_time_current(self):
        "현재 표시된 실행 시간 반환"
        qdate = [int(x) for x in self.targetTime.date().toString(
            'yyyy-MM-dd').split('-')]
        qtime = [int(x) for x in self.targetTime.time().toString(
            'hh:mm:ss').split(':')]
        return qdate + qtime

    def run(self):
        "매크로 셋팅"
        if self.target_time is None:
            pass
        current = self.targetList.currentRow()
        waiting_window = WaitingWindow(self.stack)
        self.stack.addWidget(waiting_window)
        self.macro.macro_set(self.target_time_current(), self.data[current][1])
        self.stack.setCurrentIndex(2)

    def alert(self, status, title, message):
        "메시지 얼럴트"
        action = {
            'warning': QMessageBox.warning,
            'information': QMessageBox.information,
            'critical': QMessageBox.critical,
            'about': QMessageBox.about
        }
        return action[status](self.centralwidget, title, message)
