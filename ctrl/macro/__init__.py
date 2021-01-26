
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException


class Macro:
    def __init__(self, browser):

        def set_chrome():
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-infobars")
            options.add_argument("--enable-automation")
            return webdriver.Chrome(
                "chromedriver.exe", chrome_options=options)

        def set_ie():
            # 아직 지원되지 않는다는 메시지 띄우기
            exit(-1)

        self.driver = [set_chrome, set_ie][browser]()
        self.driver.set_window_size(320, 240)

    def login(self, uid, pwd, pbar):
        pbar.setValue(50)
        self.driver.get("https://www.namyeoju.co.kr/Member/Login.aspx")
        pbar.setValue(55)
        elemId = self.driver.find_element_by_name(
            'ctl00$ContentPlaceHolder1$userID')
        elemId.clear()
        elemId.send_keys(uid)
        pbar.setValue(65)
        elemPW = self.driver.find_element_by_name(
            'ctl00$ContentPlaceHolder1$userPass')
        elemPW.clear()
        elemPW.send_keys(pwd)
        pbar.setValue(75)
        self.driver.execute_script("loginTrigger()")
        pbar.setValue(90)
        try:
            self.driver.switch_to_alert()
            pbar.hide()
            return False
        except NoAlertPresentException:
            pbar.setValue(100)
            return True