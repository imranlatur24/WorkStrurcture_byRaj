from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import requests
import logging
import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
timestamp = 1528797322
date_time = datetime.fromtimestamp(timestamp)

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
        if url_new.endswith(".html"):
            url_files.append(url_new)
    return url_files
#print(read_url("http://127.0.0.1:4433/NPTEL/"))
logging.basicConfig(
     filename = datetime.now().strftime('%d-%b-%Y.log'),
     level=logging.DEBUG,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)
engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
def fill_data(file_path):
    #logging.info('executing fill_data function')
    #print(file_path)
    try:
        #print('filepath is', file_path)
        res_nptel = requests.get(file_path)
        soup = BeautifulSoup(res_nptel.text, 'lxml')
        # print(soup)
        table = soup.find('table')
        table_rows = table.find_all('tr')
        res = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td if tr.text.strip()]
            if row:
                logging.info('nptel row by user keyword ', row)

                res.append(row)

        df = pd.DataFrame(res,
                          columns=["subject_id", "disciplineName", "subjectName", "coordinators",
                                   "filetype", "institute", "filename"])
        df["filepath"] = file_path
        logging.info(' PARENT NPTEL fill_data SQL Query executing')
        print(df)
        # df1 = df.append(df_lect)
        df.to_sql(name='parent', con=engine, if_exists='append', index=False)
        #print(df_lect)
    except:
        pass

'''def read_files(folder_path):
        for data_file in sorted(os.listdir(folder_path)):
            logging.info('folder_path results of parent_nptel')
            fill_data("http://127.0.0.1:4433/NPTEL/"+data_file)

read_files("http://127.0.0.1:4433/NPTEL/")'''

url_data=read_url("http://127.0.0.1:4433/NPTEL/")
for i in url_data:
    print('filepath ',i)
    fill_data(i)