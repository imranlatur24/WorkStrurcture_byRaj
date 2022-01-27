import logging
import os
import pandas as pd
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine
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
