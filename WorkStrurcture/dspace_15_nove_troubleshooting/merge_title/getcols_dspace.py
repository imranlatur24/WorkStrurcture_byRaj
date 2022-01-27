#1.current file is used to get daba of title by using existing parent table
#2.title is scrapped into option html tag
#3.title data managing into child_lectname tbl
#4.all lectname data is managed here
#5.here our db name is drdo/testing
#6.here our table name is child_lectname
import os
import os.path
import mysql.connector
import logging
import datetime
logging.basicConfig(
    #filename = datetime.now().strftime('%d-%b-%Y.log'),
    filename='C:/Users/3029/PycharmProjects/WorkStrurcture/WorkStrurcture/logs/merge_dspace.log',
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
logging.info('getcols_dspace file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in getcols_dspace file')
logging.debug('getcols_janes database connection establishing..in getcols_dspace FILE')


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
    logging.info('getcols table in testing db is connnected successfully in getcols_dspace file')
    cursor = my_conn.cursor()
except:
    pass
    print("testing db not connected")
    logging.info('getcols table in testing db is not connnected successfully in getcols_dspace file')

merge_arr = []
Institute_arr = []
def getdata():
    cursor.execute("SELECT DISTINCT(author) from dspace")
    author = cursor.fetchall()
    print('author type', type(author))
    for r in author:
        merge_arr.append(r)
    cursor.execute("SELECT DISTINCT(DESCRIPTION) from dspace")
    DESCRIPTION = cursor.fetchall()
    print('DESCRIPTION type', type(DESCRIPTION))
    for r in DESCRIPTION:
        merge_arr.append(r)
    cursor.execute("SELECT DISTINCT(subject) from dspace")
    subject = cursor.fetchall()
    print('subject type', type(subject))
    for r in subject:
        merge_arr.append(r)
        #print(r)
    cursor.execute("SELECT DISTINCT(TITLE) from dspace")
    TITLE = cursor.fetchall()
    print('TITLE type', type(TITLE))
    for r in TITLE:
        merge_arr.append(r)
        #print(r)
    for i in merge_arr:
        sql = "INSERT IGNORE INTO `dspace_merge`(`id`, `TITLE`) VALUES (null,%s)"
        values = (i)
        cursor.execute(sql, values)
        print(values)
        my_conn.commit()
    # Printing concatenated list
    print("Concatenated list using naive method : " + str(merge_arr))
getdata()