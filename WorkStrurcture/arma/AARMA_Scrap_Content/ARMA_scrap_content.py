#1.ARMA SCRAP CONTENT used for scrapping real time data by armablog server
#2.data get by wp_es_sentdetails columns
import logging
from bs4 import BeautifulSoup
import mysql.connector
import warnings
from datetime import datetime
import logging
warnings.filterwarnings("ignore")

logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('%d-%b-%Y.log'),
    #filename='E:/DRDO/all_project/all_project/drdo.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')# set up logging to console
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
logging.warning('ARMA_scrap_content FILE CALLING FOR SCRAPPINGS')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.warning('wordpress db connection is establishing in ARMABLOG_SCRAP CONTENT FILE')

try:
    testing_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="wordpress"
    )
    print("wordpress database connected")
    logging.debug('ARMA_scrap_content file wordpress connected')
    cursor = testing_conn.cursor()
except ConnectionRefusedError:
    print("please check your wordpress server is on")
    logging.debug('ARMA_scrap_content file db connected')
except:
    print("connection problem in wordpress database")
    logging.debug('ARMA_scrap_content file db connected')
SOURCE='armablog'
try:
    cursor.execute("select es_sent_subject,es_sent_preview from wp_es_sentdetails")
    data = cursor.fetchall()
    logging.debug('ARMA_scrap_content data array value here ',data)
    for row in data:
        logging.debug('ARMA_scrap_content data in each element ', row)
        res = ','.join([''.join(sub) for sub in row])
        soup = BeautifulSoup(res,'lxml')
        for link in soup.findAll('a'):
            print(link.string)
    cursor.execute("select es_sent_subject from wp_es_sentdetails")
    data = cursor.fetchall()
    for es_sent_subject in data:
        convert_str = ', '.join([''.join(sub) for sub in es_sent_subject])
        print(convert_str)
    logging.debug('ARMA_scrap_content scrapping completed')
except:
    pass

#ref by https://stackoverflow.com/questions/45900619/extract-link-and-text-if-certain-strings-are-found-beautifulsoup
