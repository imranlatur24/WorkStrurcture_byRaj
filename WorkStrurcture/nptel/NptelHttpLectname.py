from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import requests
import logging
import os
from datetime import datetime
import pandas as pd
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from flask_cors import CORS
import pymysql
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
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)
logging.info('Welcome To Intelligent Library Managment System')
logging.info('child_lectname file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in child_lectname file')
logging.debug('child_lectname database connection establishing..in child_lectname FILE')

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

def fill_data(file_path):
    try:
        #with open(file_path) as openfh:
            res_nptel = requests.get(file_path)
            print(file_path)
            soup = BeautifulSoup(res_nptel, 'lxml')
            print(soup)
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

url_data=read_url("http://127.0.0.1:4433/NPTEL/")
for i in url_data:
    #print('filepath ',i)
    fill_data(i)