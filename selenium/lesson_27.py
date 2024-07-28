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

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()
matches = driver.find_elements(By.TAG_NAME, 'tr')
date = []
home_team = []
score = []
away_team = []
for match in matches:
    date.append(match.find_element(By.XPATH, "./td[1]").text)
    home = match.find_element(By.XPATH, "./td[2]").text
    home_team.append(home)
    print(home)
    score.append(match.find_element(By.XPATH, "./td[3]").text)
    away_team.append(match.find_element(By.XPATH, "./td[4]").text)


time.sleep(5)

driver.quit()