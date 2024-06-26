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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class FindCourseExistence:
    def __init__(self, course, semester) -> None:
        self.course = course
        self.semester = semester
        load_dotenv()
        self._username = os.getenv("UCAL_USERNAME")
        self._password = os.getenv("UCAL_PASSWORD")

    def _setup_method(self):
        options = Options()
        options.add_argument("--headless") # dont gotta show the chrome browser
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def _teardown_method(self):
        self.driver.quit()

    def _wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def _does_course_exist(self) -> bool:
        self.driver.get(
            "https://cas.ucalgary.ca/cas/login?service=https://portal.my.ucalgary.ca/psp/paprd/?cmd=start&ca.ucalgary.authent.ucid=true"
        )

        signin_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "signinbutton"),
            )
        )

        self.driver.set_window_size(1000, 1040)
        self.driver.find_element(By.ID, "eidtext").send_keys(self._username)
        self.driver.find_element(By.ID, "passwordtext").send_keys(self._password)
        signin_button.click()
        self.vars["window_handles"] = self.driver.window_handles

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".selected > .ucSSS_ShCtVSBbtn:nth-of-type(1)")
            )
        ).click()

        new_window = self._wait_for_window(2000)
        if new_window:
            self.driver.switch_to.window(new_window)

        time.sleep(5) # for stupid loading animations
        
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".welcome_cont_but > .big_button")
            )
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, self.semester))
        ).click()

        time.sleep(5) # more stupid loading anims

        self.driver.execute_script("window.scrollTo(0,0)")

        course_search = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "code_number"))
        )

        course_search.click()

        course_search.send_keys(self.course)
        course_search.send_keys(Keys.ENTER)

        time.sleep(1) # wait just a little for error message to load

        message_area = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "message_area"))
        )

        # if message_area.text == '"CPSC 599" is only available in the term 2024 Winter.':
        if "is only available in the term" in message_area.text:
            # print(f"FOUND THE ERROR MESSAGE, {self.course} does not exist")
            return False
        else:
            # print(f"no error message, {self.course} exists!!!!!!!!")
            return True
        
    def check_course(self) -> bool:
        self._setup_method()
        course_exists = self._does_course_exist()
        self._teardown_method()
        return course_exists

