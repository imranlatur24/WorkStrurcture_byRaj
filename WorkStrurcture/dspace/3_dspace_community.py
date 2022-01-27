#https://stackoverflow.com/questions/4685173/delete-all-duplicate-rows-except-for-one-in-mysql
#how to read file from ip address using python code in windows

import os
import pandas as pd
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
#remove existing data into dspace db before scrapping and insert new one
def remove_data():
    try:
        conn = sql_conn("localhost", "root", "", "testing")
        cursor= conn.cursor()
        cursor.execute("TRUNCATE TABLE `dspace`")
        data = cursor.fetchall()
        print('data in ',data)
        print('data type ',type(data))
        if data == 0:
            resp = jsonify('dspace database deleted successfully..')
        elif data != 0:
            resp = jsonify('dspace database deleted successfully..')
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#creating connection with testing db
def sql_conn(hostname,username,password,dbname):
    myconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('connected successfully')
    return myconn

def file_scrapping(file_path):
    try:
        with open(file_path, encoding='cp437'):
            print(file_path)
            col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.identifier.uri','dc.identifier.citation[]','dc.description[]','dc.publisher[]','dc.subject[]','dc.title[]']
            df = pd.read_csv(file_path,low_memory=False,usecols=col_list)#done
            '''df.drop(index=df.index[0],
                    axis=0,
                    inplace=True)'''

            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]':'date_issued',
                               'dc.description[]':'DESCRIPTION',
                               'dc.identifier.uri': 'filepath',
                               'dc.subject[]': 'subject',
                               'dc.title[]': 'TITLE',
                               'dc.identifier.citation[]': 'citation',
                               'dc.publisher[]':'publisher',
                               }, inplace=True)
            print(df)
            df.to_sql(name='dspace', con=engine, if_exists='append',index=True)
    except:
        pass


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])

def read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        file_scrapping("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/Community/" + data_file)
#remove_csv()
#remove_data()
read_files("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/Community/")
