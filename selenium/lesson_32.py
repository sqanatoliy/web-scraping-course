import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# define the website to scrape and path where the chromediver is located and Chrome profile path
website = "https://www.audible.com/search"
chrome_profile_path = "/Users/nitort/Library/Application Support/Google/Chrome/CustomProfile"
chrome_executable_path = ChromeDriverManager().install()

chrome_service = ChromeService(executable_path=chrome_executable_path)
options = webdriver.ChromeOptions()

# add the following options to run the browser in headless mode
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument(f"user-data-dir={chrome_profile_path}")


driver = webdriver.Chrome(service=chrome_service, options=options)

# open Google Chrome with chromedriver
driver.get(website)

# Locating the box that contains all the audiobooks listed in the page
container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')

# Getting all the audiobooks listed (the "/" gives immediate child nodes)
products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
# products = container.find_elements_by_xpath('./li')

# Initializing storage
book_title = []
book_author = []
book_length = []
# Looping through the products list (each "product" is an audiobook)
for product in products:
    # We use "contains" to search for web elements that contain a particular text, so we avoid building long XPATH
    book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)  # Storing data in list
    book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
print(df_books)
df_books.to_csv('headless_books.csv', index=False)
