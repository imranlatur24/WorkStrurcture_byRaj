#1.ARMA SCRAP TITLE is used to get daba of title by using existing armablog_title2 table
#2.table name wp_es_sentdetails which is already avaialble into armablog db
#3.armablog db name is wp_es_sentdetails
#4.we are fetchting only title column from wp_es_sentdetails table which is column name is es_sent_subject as a title
#5.here our db name is drdo
#6.here our table name is armablog_title2
import mysql.connector
import logging
logging.basicConfig(
    filename='arma_scrap_title.log',
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
logging.info('armablog_scrap_title file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in armablog_scrap_title file')
logging.debug('armablog database connection establishing..in armablog_scrap_title FILE')

my_conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="testing")

def mycommon(hostname,username,password,dbname):
    armaconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('testing armablog db connected successfully')
    logging.info('testing armablog db connected successfully in ARMA_SCRAP_FILEPATH file')
    return armaconn

def truncate():
    my_cur = my_conn.cursor()
    my_cur.execute('TRUNCATE TABLE `armablog_title`')


def get_data():
    SOURCE = 'armablog'
    id = 1
    arma_conn = mycommon("localhost", "root", "", "wordpress")
    arma_cur = arma_conn.cursor()
    arma_cur.execute("select es_sent_subject from wp_es_sentdetails")
    data = arma_cur.fetchall()
    logging.debug('array data in ARMA_SCRAP_TITLE FILE ',data)
    print('data type of data ',type(data))
    try:
        id=0
        for row in data:
            TITLE = ','.join([''.join(sub) for sub in row])
            values = (TITLE)
            sliced = values[25:]
            print('sliced VALUES', sliced)
            sql = "INSERT INTO `armablog_title` (`id`, `TITLE`) VALUES (null,%s)"
            id = id + 1
            my_cur = my_conn.cursor()
            my_cur.execute(sql, (sliced,))
            print(values)
            # my_cur.commit()
            # arma_cur.commit()
    except:
        my_conn.rollback()
        print(my_cur.rowcount, "record inserted armablog_title")
        my_conn.close()
        arma_conn.close()
        logging.debug('libsys database connection closed successfully..in armablog_scrap_title FILE')
        logging.warning('armablog_scrap_title file work is completed')
truncate()
get_data()
