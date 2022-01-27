from urllib.request import Request, urlopen, urlretrieve

import requests
import logging
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
timestamp = 1528797322
date_time = datetime.fromtimestamp(timestamp)

logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('%d-%b-%Y.log'),
    #filename='E:/DRDO/all_project/all_project/drdo.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
def read_url(url):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    url_files=[]
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ","%20")
        if(file_name[-1]=='/' and file_name[0]!='.'):
            read_url(url_new)
        if url_new.endswith(".htm"):
            url_files.append(url_new)
    return url_files
#print(read_url("http://127.0.0.1:4433/janes/jalw67/"))
def file_scrapping(file_path):
    print('filepath is',file_path)
    res = requests.get(file_path)
    #print("The status code is ", res.status_code)
    #print("\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)
    #soup = BeautifulSoup(open(file_path))
            #print(file_path)
    num = []
    SOURCE = 'janes'
            #print(file_path)
    soup_str = soup.get
    Country = soup.find("meta", {"name": "Country"})['content']  # print("Country: ",Country)
    Company = soup.find("meta", {"name": "Company"})['content']  # print("Country: ",Country)
    Section = soup.find("meta", {"name": "Section"})['content']  # print("Section : ",Section)
    toc = soup.find("meta", {"name": "Toc1"})['content']
    for h2_data in soup.findAll('h2'):
        title=h2_data.get_text()
                #print(title)
        UpdateStatus = soup.find("meta", {"name": "UpdateStatus"})['content']
            # print("Title : ",title)
        date = soup.find({"p"}, {"align": "right"})
        date_conv = date.text[13:25]  # print(date_conv)
        engine = create_engine("mysql+pymysql://root@localhost/testing")
        engine.connect()
        df = pd.DataFrame({'company': [Company], 'country': [Country],'section':[Section],'general_title':[toc],'date':[date_conv],'status':[UpdateStatus],'filepath':[file_path],'SOURCE':[SOURCE],'TITLE':[title]})
        df.to_sql('hand', engine, if_exists="replace")
        #print(df)
url_data=read_url("http://127.0.0.1:4433/janes/jalw67/")
for i in url_data:
    file_scrapping(i)

