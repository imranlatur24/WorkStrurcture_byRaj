## make sure your armablog_filepath table should be UNIQUE value for vol-1 and vol-2

#1.ARMA SCRAP FILEPATH is used to get daba of filepath by using existing armablog_filepath table
#2.table name wp_es_sentdetails which is already avaialble into armablog db name is wordpress
#3.armablog db name is wp_es_sentdetails
#4.we are fetchting only filepath column from wp_es_sentdetails table which is column name is es_sent_preview as a filepath
#5.here our db name is testing
#6.here our table name is armablog_filepath
import mysql.connector
from bs4 import BeautifulSoup

import logging
logging.basicConfig(
    filename='armablog_scrap_filepath.log',
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
logging.info('armablog merge file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.warning('drdo db connection is establishing in ARMABLOG_MERGE')

my_conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="testing")

def mycommon(hostname,username,password,dbname):
    armaconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('testing armablog db connected successfully')
    logging.info('testing armablog db connected successfully in ARMA_SCRAP_FILEPATH file')
    return armaconn

def truncate():
    my_cur = my_conn.cursor()
    my_cur.execute('TRUNCATE TABLE `armablog_filepath`')

def subject_title_tbl():
    SOURCE = 'Armablog'
    id = 1
    arma_conn = mycommon("localhost", "root", "", "wordpress")
    arma_cur = arma_conn.cursor()
    arma_cur.execute("select es_sent_preview from wp_es_sentdetails")
    data = arma_cur.fetchall()
    #logging.warning('data array value in ARMA_SCRAP_FILEPATH file ',data)
    try:
        for row in data:
            res = ','.join([''.join(sub) for sub in row])
            soup = BeautifulSoup(res, 'lxml')
            for link in soup.findAll('a'):
                # print(type(link.string))
                FILEPATH = str(link.string)
                # print(type(FILEPATH))
                my_cur = my_conn.cursor()
                sql = "INSERT INTO `armablog_filepath`(`id`, `filepath`, `SOURCE`) VALUES (null,%s,%s)"
                values = (FILEPATH, SOURCE)
                my_cur.execute(sql, values)
                print(values)
                my_conn.commit()
                print(my_cur.rowcount, "record inserted.")
                #my_cur.commit()
                # arma_cur.commit()
                #logging.warning('commited successfully ')
                '''schedule.every(10).seconds.do(subject_title_tbl)
                while 1:
                    schedule.run_pending()
                    time.sleep(1)'''
    except:
        my_conn.rollback()
        print(my_cur.rowcount, "record inserted armablog filepath")
        my_conn.close()
        arma_conn.close()
        logging.warning('drdo db connection closed succesfully in ARMA_SCRAP_FILEPATH file')
        logging.warning('ARMA_SCRAP_FILEPATH file work is completed')


truncate()
subject_title_tbl()
