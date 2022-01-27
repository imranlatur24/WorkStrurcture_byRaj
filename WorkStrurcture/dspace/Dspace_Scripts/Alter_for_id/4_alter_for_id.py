import logging
import os
import pandas as pd
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine
from datetime import datetime
logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('Alter_for_id-%d-%b-%Y.log'),
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
#creating connection with testing db
def sql_conn(hostname,username,password,dbname):
    myconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('connected successfully')
    return myconn

engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
#remove existing data into dspace db before scrapping and insert new one
def add_id():
    try:
        conn = sql_conn("localhost", "root", "", "testing")
        cursor= conn.cursor()
        cursor.execute(
            "UPDATE dspace SET filepath = REPLACE(filepath, 'http://localhost:8080', 'http://128.9.32.52:8080')")
        print('filepath succesfully updated with http://128.9.32.52:8080')

        cursor.execute(
            "UPDATE dspace SET date_issued = REPLACE(date_issued, '0', ' ')")
        print('0 replaced successfully')

        cursor.execute(
            "UPDATE dspace SET date_issued = REPLACE(date_issued, '-', ' ')")
        print('-  replaced successfully')

        cursor.execute("ALTER TABLE `dspace` ADD `id` INT(11) NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`)")
        print('autoincrement added into dspace db ')

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
add_id()
