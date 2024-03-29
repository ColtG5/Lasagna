import time
import asyncio
import os
from dotenv import load_dotenv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class FindCpsc599:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def does_cpsc599_exist(self) -> bool:
        load_dotenv()
        self.driver.get(
            "https://cas.ucalgary.ca/cas/login?service=https://portal.my.ucalgary.ca/psp/paprd/?cmd=start&ca.ucalgary.authent.ucid=true"
        )
        time.sleep(2)
        self.driver.set_window_size(1000, 1040)
        self.driver.find_element(By.ID, "eidtext").send_keys(os.getenv("UCAL_USERNAME"))
        self.driver.find_element(By.ID, "passwordtext").send_keys(
            os.getenv("UCAL_PASSWORD")
        )
        self.driver.find_element(By.ID, "signinbutton").click()
        time.sleep(5)
        # 6 | click | css=.isSSS_ShCtTermWrp:nth-child(6) |  |
        # self.driver.find_element(By.CSS_SELECTOR, ".isSSS_ShCtTermWrp:nth-child(2)").click()
        # 7 | click | css=.selected > .ucSSS_ShCtVSBbtn:nth-child(2) |  |
        self.vars["window_handles"] = self.driver.window_handles
        time.sleep(4)
        # 8 | selectWindow | handle=${win3707} |  |
        self.driver.find_element(
            By.CSS_SELECTOR, ".selected > .ucSSS_ShCtVSBbtn:nth-child(2)"
        ).click()
        # 9 | click | css=.reg_welcome |  |
        self.vars["win3707"] = self.wait_for_window(2000)
        # 10 | click | css=.welcome_cont_but > .big_button |  |
        self.driver.switch_to.window(self.vars["win3707"])
        time.sleep(5)
        # 12 | click | linkText=2024 Fall |  |
        self.driver.find_element(
            By.CSS_SELECTOR, ".welcome_cont_but > .big_button"
        ).click()
        time.sleep(1)
        # 14 | click | id=code_number |  |
        self.driver.find_element(By.LINK_TEXT, "2024 Fall").click()
        time.sleep(6)
        # 15 | type | id=code_number | cpsc 599 |
        self.driver.execute_script("window.scrollTo(0,0)")
        # 16 | sendKeys | id=code_number | ${KEY_ENTER} |
        self.driver.find_element(By.ID, "code_number").click()
        self.driver.find_element(By.ID, "code_number").send_keys("cpsc 599")
        self.driver.find_element(By.ID, "code_number").send_keys(Keys.ENTER)
        time.sleep(2)

        message_area = self.driver.find_element(By.ID, "message_area")

        # <div class="warningNoteBad note6 takespace" style=""><span>"CPSC 599" is only available in the term 2024 Winter.</span></div>

        # warning_elements = message_area.find_elements(By.XPATH, ".//span[contains(text(), 'CPSC 599 is only available in the term 2024 Winter.')]")

        # print(message_area.text)

        # print(message_area)

        if message_area.text == '"CPSC 599" is only available in the term 2024 Winter.':
            print("FOUND THE ERROR MESSAGE, course does not exist")
            return False
        else:
            print("no error message, course exists!!!!!!!!")
            return True

