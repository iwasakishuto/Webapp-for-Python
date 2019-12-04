# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,1024')

BY_ELEMENTS = [v for k,v in By.__dict__.items() if k[0]!="_"]

class SeleniumChrome():
    def __init__(self, executable_path="chromedriver", port=0):
        self.driver = webdriver.Chrome(executable_path=executable_path, port=port, chrome_options=options)
        self.driver.maximize_window()
        self.email = None
        self.password = None

    @staticmethod
    def _checkByElements(by, element):
        if by not in BY_ELEMENTS:
            raise KeyError(f"Please select `tag` from {', '.join(BY_ELEMENTS)}")
        locator = (by, element)
        return locator

    def align2fnFormat(self, fn=None, extentions=".png"):
        if fn is None:
            fn = self.driver.title + extentions
        elif not fn.endswith(extentions):
            fn += extentions
        print(f"Filename: {fn}")
        return fn

    def waitUnitilElement(self, by, element, wait_time=30):
        locator = self._checkByElements(by, element)
        WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
        time.sleep(1) # Additional wait time.

    def fill(self, by, element, content):
        locator = self._checkByElements(by, element)
        self.driver.find_element(*locator).send_keys(content)
        time.sleep(1) # Additional wait time.

    def select(self, by, element, value):
        locator = self._checkByElements(by, element)
        select_element = self.driver.find_element(*locator)
        select_element = Select(select_element)
        select_element.select_by_value(value)

    def click(self, by, element):
        locator = self._checkByElements(by, element)
        self.driver.find_element(*locator).click()
        time.sleep(1) # Additional wait time.

    def takeScreenShot(self, fn=None):
        fn = self.align2fnFormat(fn, extentions=".png")
        self.driver.save_screenshot(fn)

    def getPageSource(self, fn=None):
        fn = self.align2fnFormat(fn, extentions=".html")
        html = self.driver.page_source
        with open(fn, mode="w", encoding="utf-8") as f:
            f.write(html)

    def loginGoogleAccount(self, email, password, google_url='https://www.google.com/accounts'):
        self.driver.get(google_url)
        #=== Email Address ===
        self.waitUnitilElement(by="name", element="Email") # element="identifier"
        self.fill(by="name", element="Email", content=email)
        # self.click(by="name", element="signIn")
        self.driver.find_element_by_name("signIn").click()

        #=== Pass Word ===
        self.waitUnitilElement(by="name", element="Passwd")
        self.fill(by="name", element="Passwd", content=password)
        # self.click(by="name", element="signIn")
        self.driver.find_element_by_name("signIn").click()

        time.sleep(5)
        self.email = email
        self.password = password

    def ansGoogleForm(self, form_url, screenshot=True, default="お肉が食べたいです。", **formkwargs):
        filename = form_url.split('/')[-1] + ".png"
        form_q_class   = "quantumWizTextinputPaperinputInput"
        form_btn_class = "quantumWizButtonPaperbuttonLabel"

        self.driver.get(form_url)
        self.waitUnitilElement(by="class name", element=form_q_class, wait_time=30)
        time.sleep(5)

        for question in self.driver.find_elements_by_class_name(form_q_class):
            question.send_keys(formkwargs.get(question.get_attribute("type"), default))

        if screenshot:
            self.takeScreenShot(fn=filename)
        self.click(by="class name", element=form_btn_class)
        time.sleep(5)
        return filename
