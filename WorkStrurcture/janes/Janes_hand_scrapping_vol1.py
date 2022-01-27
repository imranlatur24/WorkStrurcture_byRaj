## make sure your hand table should be UNIQUE value for vol-1 and vol-2

#1.in this file we are scrapping first volume which is named is Jane's Handbook
#2.once scrapping is done data will be avialble on hand table which is located into testing/drdo db
#3.janes work is completed here.

import logging
from bs4 import BeautifulSoup
import mysql.connector
import os,os.path
logging.basicConfig(
    filename='C:/Users/3029/PycharmProjects/WorkStrurcture/WorkStrurcture/logs/janes_vol1.log',
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
logging.info('JANES HAND VOL 1 FILE CALLING FOR SCRAPPINGS')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.info('database connection initializing')
def sql_conn(hostname,username,password,dbname):
    myconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('connected successfully')
    logging.info('database connected successfully for in JANES VOL-1 FILE ',)
    return myconn
#working with beautifulsoup
def file_scrapping(file_path):
    try:
        soup = BeautifulSoup(open(file_path))
        logging.debug('soup data ',soup)
        num=0
        SOURCE='janes'
        print(file_path)
        logging.debug('received filepath vol-1 ', file_path)
        soup_str = soup.get
        #print(soup_str)
        Country = soup.find("meta", {"name":"Country"})['content']#print("Country: ",Country)
        logging.debug('received filepath vol-1 Country ', Country)
        Company = soup.find("meta", {"name":"Company"})['content']#print("Country: ",Country)
        logging.debug('received filepath vol-1 Company ', Company)
        Section = soup.find("meta", {"name":"Section"})['content'] #print("Section : ",Section)
        logging.debug('received filepath vol-1 Section ', Section)
        toc = soup.find("meta", {"name":"Toc1"})['content']
        logging.debug('received filepath vol-1 toc ', toc)
        title = soup.find("meta", {"name":"Publication"})['content']
        logging.debug('received filepath vol-1 title ', title)
        UpdateStatus = soup.find("meta", {"name":"UpdateStatus"})['content']#print("Title : ",title)
        logging.debug('received filepath vol-1 UpdateStatus ', UpdateStatus)
        date  = soup.find({"p"},{"align":"right"})
        logging.debug('received filepath vol-1 date ', date)
        date_conv = date.text[13:25]#print(date_conv)
        logging.debug('received filepath vol-1 date_conv ', date_conv)
        conn = sql_conn("localhost","root","","drdo")
        # creating the cursor object
        cur = conn.cursor()
        sql = "INSERT INTO hand VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
        val = (num, Company, Country, Section, title, date_conv, UpdateStatus, file_path,"","","",SOURCE,"",Company)
        num=num+1
        # inserting the values into the table
        cur.execute(sql, val)
        # commit the transaction
        conn.commit()
        logging.info('database commited in vol 1')
        #conn.close()
        logging.warning('JANES HAND VOL 1 FILE SCRAPPINGS DONE HERE')
    except Exception as e:
        print(e)
        logging.exception('exception in vol 1 ',e)
    except OSError as filenotfoundex:
        print(filenotfoundex)
        logging.exception(' filenotfoundex exception in vol 1 ', filenotfoundex)
    finally:
        cur.close()
        logging.warning('finally block executed successfully cursor closed in vol 1')
        conn.close()
        logging.warning(' finally block executed successfully database closed in vol 1')
        logging.warning('JANES HAND VOL 1 FILE work is completed')
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        file_scrapping("D:/Jens_Handbook/browse/binder/jalw/jalw67/"+data_file)
        logging.warning('data_file in vol 1',data_file)
'''
def main(folder):
    number = count_files(folder)
    for data in range(number): '''
read_files("D:/Jens_Handbook/browse/binder/jalw/jalw67")
logging.warning('read_files() in vol 1')



