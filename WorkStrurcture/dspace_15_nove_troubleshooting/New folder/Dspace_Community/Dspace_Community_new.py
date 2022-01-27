import os
import pandas as pd
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine
from datetime import datetime
import logging

logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('DSPACE_Collection_New-%d-%b-%Y.log'),
    #filename='E:/DRDO/all_project/all_project/drdo.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
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
logging.info('getcols_dspace file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in getcols_dspace file')
logging.debug('getcols_janes database connection establishing..in getcols_dspace FILE')

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
            col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.identifier.uri','dc.description.provenance[en]','dc.publisher[]','dc.subject[]','dc.title[]']
            df = pd.read_csv(file_path,low_memory=False,usecols=col_list)#done
            df.drop(index=df.index[0],
                    axis=0,
                    inplace=True)

            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]':'date_issued',
                               'dc.description.provenance[en]':'DESCRIPTION',
                               'dc.identifier.uri': 'filepath',
                               'dc.publisher[]': 'publisher',
                               'dc.subject[]': 'subject',
                               'dc.title[]': 'TITLE',

                               }, inplace=True)
            print(df)
            df.to_sql(name='dspace', con=engine, if_exists='append',index=False)
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
