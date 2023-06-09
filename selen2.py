import time
import sys
import csv 
import pandas
import requests
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
url1 = "https://www.teegschwendner.de/"
re = requests.get(url1)
print(re.status_code)
soup = BeautifulSoup(re.content, 'html.parser')
urls = soup.find("div", class_="home-tea-categories-inner row").find_all("a")
base_url = "https://www.teegschwendner.de/"
all_url = []
all_categories = []
categories_info = []
for x in urls:
    url = x.get("href")
    k = base_url+str(url)
    categor = x.find("h3").text.strip()
    info = x.find("p").text.strip()
    all_categories.append(categor)
    categories_info.append(info)
    all_url.append(k)


scraped = []
for f in range(len(all_url)):
    url = all_url[f]
    cetegoria = all_categories[f]
    categorie_info = categories_info[f]
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    element = driver.execute_script("""return document.querySelector('div[id="usercentrics-root"]').shadowRoot.querySelector("button[data-testid='uc-accept-all-button']")""")
    element.click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    names = soup.find_all("div", class_="product-info")
    for x in names:
        name = x.find("a").text.strip()
        kg = x.find("div", class_="product-detail-configurator-options").find_all("option")[0].text.strip()
        price = x.find("span", class_="product-price").text.strip()
        scraped.append(
            {
            "categorea": cetegoria,
            "categorie_info": categorie_info,
            "name": name,
            "kg": kg,
            "price": price
            }
        )
df = pandas.DataFrame(data=scraped)
df.to_csv("sample.csv", index=False)
