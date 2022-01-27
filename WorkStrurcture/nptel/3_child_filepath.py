#1.current file is used to get daba of filepath by using existing parent table
#2.filepath is scrapped into option html tag
#3.filepath data managing into child_real tbl
#4.all filepath data is managed here
#5.here our db name is drdo/testing
#6.here our table name is child_real
import os
import os.path
import mysql.connector
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import logging
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import requests
from datetime import datetime
logging.basicConfig(
    filename=datetime.now().strftime('%d-%b-%Y.log'),
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
logging.debug('drdo database establishing in child_filepath file')
logging.debug('child_real database connection establishing..in child_filepath FILE')

engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
try:
    my_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="testing",
        connect_timeout=2000,
        buffered=True
    )
    print("np db connected in child_filepath")
    logging.error('child_filepath table in np db is connnected successfully in child_filepath file')
    cursor = my_conn.cursor()
except:
    pass
    print("drdo db not connected in child_filepath")
    logging.error('child_filepath table in np db is not connnected successfully in child_filepath file')

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
    try:
            res_nptel = requests.get(file_path)
            soup = BeautifulSoup(res_nptel.text, 'lxml')
            table = soup.find('table')
            table_rows = table.find_all('tr')
            res = []
            #check globar var cond
            i=0
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text.strip() for tr in td if tr.text.strip()]
                if row:
                    res.append(row)
                    if i==0:
                            df = pd.DataFrame(row, columns=['subject_id'])
                            sub_id = df['subject_id'].values[0]
                            #data fetched from parent class first run parent script then only try child_filepath script
                            cursor.execute("SELECT id FROM parent WHERE subject_id=%s;" % sub_id)
                            result = cursor.fetchone()
                            temp = result[0]
                            #print(temp)
                            #print(temp2)
                    demo = [option['value'] for option in soup.find_all('option')]
                    #remove # from html scrapping file
                    removetable = str.maketrans('', '', '#')
                    out_list = [s.translate(removetable) for s in demo]
                    result = [[]]
                    for item in out_list:
                        if not item:  # pass empty array where record is not found
                            result.append([])
                        else:  # pass where item got record as per corresponding id
                            result[-1].append(item)
                    list2 = [x for x in result if x != []]
                    #allow id only one time
                    id = temp
                    #print("id", id)
                    #execute for loop n no of times n means total length of current html page records
                    for i in list2:
                        df_lect = pd.DataFrame(i, columns=['lect_path'])
                        df_lect['sid'] = id

                        #coordinators
                        cursor.execute("SELECT coordinators FROM parent WHERE id=%s;" % id)
                        result = cursor.fetchone()
                        coordinators = result[0]
                        print(coordinators)
                        df_lect['coordinators'] = coordinators

                        # filetype
                        cursor.execute("SELECT filetype FROM parent WHERE id=%s;" % id)
                        result = cursor.fetchone()
                        filetype = result[0]
                        print(filetype)
                        df_lect['filetype'] = filetype

                        # institute
                        cursor.execute("SELECT institute FROM parent WHERE id=%s;" % id)
                        result = cursor.fetchone()
                        institute = result[0]
                        print(institute)
                        df_lect['institute'] = institute

                        # disciplineName
                        cursor.execute("SELECT disciplineName FROM parent WHERE id=%s;" % id)
                        result = cursor.fetchone()
                        disciplineName = result[0]
                        print(disciplineName)
                        df_lect['disciplineName'] = disciplineName

                        # subjectName
                        cursor.execute("SELECT subjectName FROM parent WHERE id=%s;" % id)
                        result = cursor.fetchone()
                        subjectName = result[0]
                        print(subjectName)
                        df_lect['subjectName'] = subjectName

                        print(df_lect)
                        #print('done')
                        id = id + 1
                        df_lect.to_sql(name='child_real', con=engine, if_exists='append', index=True)
                        logging.warning('child_filepath file work is completed')
                    break
    except:
        pass
'''def read_files(folder_path):
        for data_file in sorted(os.listdir(folder_path)):
            fill_data("E:/DRDO/NPTEL/"+data_file)
read_files("E:/DRDO/NPTEL/")'''


r=read_url("http://127.0.0.1:4433/NPTEL/")
#print(r)
for i in r:
    fill_data(i)