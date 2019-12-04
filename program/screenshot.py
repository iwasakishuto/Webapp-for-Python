from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')

driver = webdriver.Chrome('chromedriver', chrome_options=options)

driver.get('https://www.google.co.jp')
driver.save_screenshot('screenshot.png')
driver.quit()
