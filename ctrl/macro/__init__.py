"매크로 동작 관리"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, WebDriverException

from .check_time import check_time
from .time_sync import time_sync


class Status:
    "0: 정상, -1: 드라이버 없음, -2: 로그인 실패, -3: 인터넷 연결 안됨"

    def __init__(self, success=True, code=0):
        self.success = success
        self.code = code


class Macro:
    "기본적인 매크로의 동작을 정의"

    def __init__(self, browser):

        def set_chrome():
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-infobars")
            options.add_argument("--enable-automation")
            return webdriver.Chrome(
                "driver/chromedriver.exe", chrome_options=options)

        def set_ie():
            return None

        self.driver = [set_chrome, set_ie][browser]()
        if self.driver is not None:
            self.driver.set_window_size(320, 240)

    def login(self, uid, pwd, pbar):
        "로그인 동작 + 프로그래스 바"
        if self.driver is None:
            pbar.hide()
            return Status(False, -1)
        pbar.setValue(50)
        try:
            self.driver.get("https://www.namyeoju.co.kr/Member/Login.aspx")
        except WebDriverException:
            pbar.hide()
            return Status(False, -3)
        pbar.setValue(55)
        elem_id = self.driver.find_element_by_name(
            'ctl00$ContentPlaceHolder1$userID')
        elem_id.clear()
        elem_id.send_keys(uid)
        pbar.setValue(65)
        elem_pw = self.driver.find_element_by_name(
            'ctl00$ContentPlaceHolder1$userPass')
        elem_pw.clear()
        elem_pw.send_keys(pwd)
        pbar.setValue(75)
        self.driver.execute_script("loginTrigger()")
        pbar.setValue(90)
        try:
            self.driver.switch_to_alert()
            pbar.hide()
            return Status(False, -2)
        except NoAlertPresentException:
            pbar.setValue(100)
            return Status(True, 0)

    def macro_set(self, target, script):
        "sec초 후 script 실행!"

        def func():
            self.driver.set_window_size(1024, 768)
            self.driver.execute_script(script)

        wait_sec = time_sync(target)
        check_time(wait_sec, func)
