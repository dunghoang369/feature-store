import os
import subprocess
import time
from glob import glob

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

service = Service(
    executable_path="/home/dunghoang300699/chromedriver_linux64/chromedriver"
)

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)

# Scroll to the end of the page
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
# time.sleep(2)

elements_questions = driver.find_elements(By.CLASS_NAME, "faq-questions")
tables = glob("data/*.parquet")
tables = [table.split("/")[-1] for table in tables]
print(tables)
# for i, element in enumerate(elements_questions):
#     element.click()
#     page = BeautifulSoup(driver.page_source, features="html.parser")
#     links = page.find_all("a", {"class": "exitlink"})
#     for link in links:
#         link = link['href']
#         if link.endswith(".parquet") and link not in tables:
#             subprocess.run(f"wget {link}", shell=True, check=True)
#             subprocess.run(f"mv *.parquet data/", shell=True, check=True)
#     time.sleep(15)

# time.sleep(10)
# driver.quit()
