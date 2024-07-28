import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# define the website to scrape and path where the chromediver is located and Chrome profile path
web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=adc4b13b-d074-4e1c-ac46-9f54aa53072b&pf_rd_r=1F7DV0MPHV77Z61RX566"
# web = "https://www.audible.com/search"
chrome_profile_path = "/Users/nitort/Library/Application Support/Google/Chrome/CustomProfile"
chrome_executable_path = ChromeDriverManager().install()

chrome_service = ChromeService(executable_path=chrome_executable_path)
options = webdriver.ChromeOptions()

# add the following options to run the browser in headless mode
# options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument(f"user-data-dir={chrome_profile_path}")


driver = webdriver.Chrome(service=chrome_service, options=options)

# open Google Chrome with chromedriver
driver.get(web)
driver.maximize_window()

# Pagination 1
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')  # locating pagination bar
pages = pagination.find_elements(By.TAG_NAME, 'li')  # locating each page displayed in the pagination bar
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

book_title = []
book_author = []
book_length = []

# Pagination 2
current_page = 1   # this is the page the bot starts scraping

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(2)  # let the page render correctly
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
    # products = container.find_elements_by_xpath('./li')

    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
    try:
        next_page = driver.find_element(By.XPATH, './/span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)