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
logging.basicConfig(
    filename='merge_all.log',
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
logging.info('autosuggestion_all file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in autosuggestion_all file')
logging.debug('testing database connection establishing..in autosuggestion_all FILE')

try:
    my_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        db="testing",
        connect_timeout=2000,
        buffered=True
    )
    print("testing db connected")
    logging.info('getcols table in testing db is connnected successfully in autosuggestion_all file')
    cursor = my_conn.cursor()
except:
    pass
    print("testing db not connected")
    logging.info('getcols table in testing db is not connnected successfully in autosuggestion_all file')

merge_arr = []
Institute_arr = []
def getdata():
    cursor.execute("SELECT DISTINCT(TITLE) from dspace_merge")
    dspace_merge = cursor.fetchall()
    print('dspace_merge type', type(dspace_merge))
    for r in dspace_merge:
        merge_arr.append(r)

    for i in merge_arr:
        sql = "INSERT IGNORE INTO `all_merge`(`id`, `TITLE`) VALUES (null,%s)"
        values = (i)
        cursor.execute(sql, values)
        print(values)
        my_conn.commit()
    # Printing concatenated list
    print("Concatenated list using naive method : "
          + str(merge_arr))

getdata()