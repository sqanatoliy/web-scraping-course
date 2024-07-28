import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# define the website to scrape and path where the chromediver is located and Chrome profile path
website = "https://www.adamchoi.co.uk/overs/detailed"
chrome_profile_path = "/Users/nitort/Library/Application Support/Google/Chrome/CustomProfile"
chrome_executable_path = ChromeDriverManager().install()

chrome_service = ChromeService(executable_path=chrome_executable_path)
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}")

driver = webdriver.Chrome(service=chrome_service, options=options)

# open Google Chrome with chromedriver
driver.get(website)

# locate and click on a button
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# select elements in the table
matches = driver.find_elements(By.TAG_NAME, 'tr')

# storage data in lists
date = []
home_team = []
score = []
away_team = []

# looping through the matches list
for match in matches:
    date.append(match.find_element(By.XPATH, "./td[1]").text)
    home = match.find_element(By.XPATH, "./td[2]").text
    home_team.append(home)
    # print(home)
    score.append(match.find_element(By.XPATH, "./td[3]").text)
    away_team.append(match.find_element(By.XPATH, "./td[4]").text)
time.sleep(5)

# quit drive we opened at the beginning
driver.quit()

# Create Dataframe in Pandas and export to CSV (Excel)
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)
