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

class FindOpenWaitlist:
    def __init__(self, course, semester) -> None:
        self.course = course
        self.semester = semester
        load_dotenv()
        self._username = os.getenv("UCAL_USERNAME")
        self._password = os.getenv("UCAL_PASSWORD")

    def setup_method(self):
        options = Options()
        options.add_argument("--headless") # dont gotta show the chrome browser
        options.add_argument("--log-level=3")
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def _is_waitlist_open(self) -> bool:
        self.driver.get(
            "https://cas.ucalgary.ca/cas/login?service=https://portal.my.ucalgary.ca/psp/paprd/?cmd=start&ca.ucalgary.authent.ucid=true"
        )

        signin_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "signinbutton"),
            )
        )

        # self.driver.set_window_size(1800, 1040)
        # self.driver.fullscreen_window()
        self.driver.find_element(By.ID, "eidtext").send_keys(self._username)
        self.driver.find_element(By.ID, "passwordtext").send_keys(self._password)
        signin_button.click()

        self.vars["window_handles"] = self.driver.window_handles

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".selected > .ucSSS_ShCtVSBbtn:nth-of-type(1)")
            )
        ).click()

        new_window = self.wait_for_window(2000)
        if new_window:
            self.driver.switch_to.window(new_window)

        # This is needed because of some stupid loading animation
        time.sleep(5)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".welcome_cont_but > .big_button")
            )
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, self.semester))
        ).click()

        # This is needed because of other stupid loading animation
        time.sleep(5)

        self.driver.execute_script("window.scrollTo(0,0)")

        course_search = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "code_number"))
        )

        course_search.click()

        course_search.send_keys(self.course)
        course_search.send_keys(Keys.ENTER)

        # Need to wait for the message to load
        time.sleep(1)

        course_exists = False
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "warningNoteBad"))
            )
        except Exception:
            course_exists = True

        if course_exists:
            course_boxes = self.driver.find_elements(By.CLASS_NAME, "course_box")

            for cool_course in course_boxes:
                if self.course in cool_course.text:
                    # Check seats for the class
                    # need a better way to check these separately
                    try:
                        seat_count = cool_course.find_element(By.CLASS_NAME, "seatText")
                        if "Full" not in seat_count.text:
                            print("class has open seats")
                            return True
                    except Exception:
                        try:
                            waitlist_count = cool_course.find_element(
                                By.CLASS_NAME, "waitText"
                            )

                            if (
                                "Full" not in waitlist_count.text
                                or "None" not in waitlist_count.text
                            ):
                                print("Class has open waitlist")
                                return True
                        except Exception:
                            print("Class is full!!")
                            return False

        print("Class doesn't exist or you are already enrolled")
        return False

    def check_course(self) -> bool:
        self.setup_method()
        course_exists = self._is_waitlist_open()
        self.teardown_method()
        return course_exists