from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.fundsexplorer.com.br/ranking")

for tr in driver.find_elements_by_tag_name("tr"):
    for td in tr.find_elements_by_tag_name("td"):
        print(td.get_attribute("innerText"))