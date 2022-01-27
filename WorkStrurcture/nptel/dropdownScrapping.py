from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
url = ('http://127.0.0.1:4433/NPTEL/aer1.html')
browser.get(url)
html_source = browser.page_source
browser.quit()
soup = BeautifulSoup(html_source, 'html.parser')
for name_list in soup.find_all(class_ ='dropdown-row'):
    print(name_list.text)