#1.current file is used to get daba of title by using existing parent table
#2.title is scrapped into option html tag
#3.title data managing into child_lectname tbl
#4.all lectname data is managed here
#5.here our db name is drdo/testing
#6.here our table name is child_lectname
import os
import os.path
import mysql.connector
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import logging
logging.basicConfig(
    filename = datetime.now().strftime('%d-%b-%Y.log'),
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
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
        host="127.0.0.1",
        user="root",
        password="",
        db="testing",
        connect_timeout=2000,
        buffered=True
    )
    print("testing db connected")
    logging.log('child_lectname table in np db is connnected successfully in child_lectname file')
    cursor = my_conn.cursor()
except:
    pass
    print("testing db not connected")
    logging.log('child_lectname table in np db is not connnected successfully in child_lectname file')

#first run parent script then only run child_lectname table script
engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
def fill_data(file_path):
    try:
        with open(file_path) as openfh:
            print(file_path)
            soup = BeautifulSoup(openfh, 'lxml')
            table = soup.find('table')
            table_rows = table.find_all('tr')
            logging.debug('data array value in child_lectname file ',table_rows)

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
                                    logging.warning('child_lectname file work is completed')

                        break
    except:
        pass
def read_files(folder_path):
        for data_file in sorted(os.listdir(folder_path)):
            fill_data("E:/DRDO/NPTEL/"+data_file)
            print(data_file)
read_files("E:/DRDO/NPTEL")