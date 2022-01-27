import logging
import os
import pandas as pd
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine
from datetime import datetime
import logging

logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('%d-%b-%Y.log'),
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
dbname = "testing"
#creating connection with testing db
# 1. check db name
# 2. check auto_increment is available in dspace-done no changes
# 3. make sure all csv file scrap into db -done
# 4. make sure uri replace with localhost to ip
# 5. remove index and citiation cols in dspace db

def sql_conn(hostname,username,password,dbname):
    myconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('connected successfully')
    logging.info('connected succesfully in 2_dpsace_merge_completed file')
    logging.debug('myconn data ',myconn)
    return myconn
###################################################
engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
#remove existing data into dspace db before scrapping and insert new one

def add_id():
    try:
        conn = sql_conn("localhost", "root", "", dbname)
        cursor= conn.cursor()
        # cursor.execute("ALTER TABLE `dspace` ADD `id` INT(11) NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`)")
        # print('autoincrement added into dspace db ')

        cursor.execute('SELECT id FROM dspace ORDER BY id DESC LIMIT 1')
        limit_lectname = cursor.fetchone()
        dspace_last = limit_lectname[0]
        logging.debug('dspace max length ', dspace_last)
        print(dspace_last)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
def replace_zero():
    try:
        conn = sql_conn("localhost", "root", "",dbname)
        cursor= conn.cursor()
        cursor.execute("UPDATE dspace SET date_issued = REPLACE(date_issued,'0',' ')")
        print('remove successfully zero from dspace table ')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
def replace_dash():
    try:
        conn = sql_conn("localhost", "root", "",dbname)
        cursor= conn.cursor()
        cursor.execute("UPDATE dspace SET date_issued = REPLACE(date_issued,'-','')")
        print('remove successfully dash from dspace table ')

        cursor.execute("UPDATE dspace SET filepath= REPLACE(filepath,'http://localhost:8080','http://128.9.32.52:8080')")
        print("Filepath Successfully Updated with http://128.9.32.52:8080'")

        cursor.execute("UPDATE dspace SET SOURCE = 'dspace'")
        print('update source column with dspace name')

    except Exception as e:
        print(e)
    finally:
        # cursor.execute(
        #     'DELETE n1 FROM dspace n1, dspace n2 WHERE n1.id > n2.id AND n1.TITLE = n2.TITLE')
        # print('duplication deleted successfully..')
        #
        # cursor.execute("delete from dspace where TITLE=''")
        # print('blank spaces removed sucessfully..')
        cursor.close()
        #
        conn.commit()
        conn.close()

add_id()
replace_zero()
replace_dash()

