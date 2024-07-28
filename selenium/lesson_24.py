import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

website = "https://www.adamchoi.co.uk/overs/detailed"

chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/nitort/Library/Application Support/Google/Chrome/CustomProfile")

driver = webdriver.Chrome(service=chrome_service, options=options)
driver.get(website)

all_matches_button = driver.find_element(By.CSS_SELECTOR, 'label[analytics-event="All matches"]')
all_matches_button.click()
time.sleep(10)
driver.quit()
