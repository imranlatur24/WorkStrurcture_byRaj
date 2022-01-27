import os
import os.path
import mysql.connector
import pandas as pd
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine

try:
    my_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        db="testing",
        connect_timeout=2000,
        buffered=True
    )
    #print("np db connected")
    cursor = my_conn.cursor()
except:
    pass
    print("np db not connected")
#first run parent script then only run child_lectname table script
engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()

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
def fill_data(file_path):
    #print(file_path)
    try:
            res = requests.get(file_path)
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('table')
            table_rows = table.find_all('tr')
            res = []
            i = 0
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text.strip() for tr in td if tr.text.strip()]
                if row:
                    res.append(row)
                    if i == 0:
                        df = pd.DataFrame(row, columns=['subject_id'])
                        sub_id = df['subject_id'].values[0]
                        cursor.execute("SELECT id FROM parent WHERE subject_id=%s;" % sub_id)
                        result = cursor.fetchone()
                        temp = result[0]
                        #print('temp', temp)
                        for tr in table_rows:
                            td = tr.find_all('option')
                            row2 = [tr.text.strip() for tr in td if tr.text.strip()]
                            if row2:
                                res.append(row2)
                                if temp > 0:
                                    df = pd.DataFrame(row2, columns=['lect_name'])
                                    print(df)
                                    df['sid'] = temp
                                    print(df[1:])
                                    temp = temp+1
                                    #df[1:] use for remove 0th position index
                                    df[1:].to_sql(name='child_lectname', con=engine, if_exists='append', index=False)
                        break
    except:
        pass

'''def read_files(folder_path):
        for data_file in sorted(os.listdir(folder_path)):
            fill_data("E:/DRDO/NPTEL/"+data_file)
            print(data_file)

read_files("E:/DRDO/NPTEL")'''
r=read_url("http://127.0.0.1:4433/NPTEL/")
#print(r)
for i in r:
    fill_data(i)
