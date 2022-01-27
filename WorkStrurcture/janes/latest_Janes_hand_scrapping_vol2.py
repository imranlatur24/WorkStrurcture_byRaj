## make sure your hand table should be UNIQUE value for vol-1 and vol-2

#1.in this file we are scrapping all volume which is named is Jane's Handbook and other 9's vol
#2.once scrapping is done data will be avialble on hand table which is located into testing/drdo db
#3.janes work is completed here.
#4.finally we are performing search operation here
import logging
from bs4 import BeautifulSoup
import os,os.path
from sqlalchemy import create_engine
import pandas as pd
import warnings
import datetime
warnings.filterwarnings("ignore")
timestamp = 1528797322
date_time = datetime.fromtimestamp(timestamp)
logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('%d-%b-%Y.log'),
    #filename='E:/DRDO/all_project/all_project/drdo.log',
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
logging.warning('JANES HAND VOL 2 FILE CALLING FOR SCRAPPINGS')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.warning('hand2 in JANES HAND VOL 2 is db is establishing')
def file_scrapping(file_path):
    try:
        soup = BeautifulSoup(open(file_path))
        logging.debug('soup data ', soup)
        num = []
        SOURCE = 'janes'
        print(file_path)
        logging.debug('received filepath vol-2 ', file_path)
        soup_str = soup.get
        Country = soup.find("meta", {"name": "Country"})['content']  # print("Country: ",Country)
        logging.debug('received filepath vol-2 Country ', Country)
        Company = soup.find("meta", {"name": "Company"})['content']  # print("Country: ",Country)
        logging.debug('received filepath vol-2 Country ', Company)
        Section = soup.find("meta", {"name": "Section"})['content']  # print("Section : ",Section)
        logging.debug('received filepath vol-2 Country ', Section)
        toc = soup.find("meta", {"name": "Toc1"})['content']
        logging.debug('received filepath vol-2 Country ', toc)
        for h2_data in soup.findAll('h2'):
            title=h2_data.get_text()
            print(title)
            UpdateStatus = soup.find("meta", {"name": "UpdateStatus"})['content']
            logging.debug('received filepath vol-2 Country ', UpdateStatus)
        # print("Title : ",title)
            date = soup.find({"p"}, {"align": "right"})
            logging.debug('received filepath vol-2 Country ', date)
            date_conv = date.text[13:25]  # print(date_conv)
            logging.debug('received filepath vol-2 Country ', date_conv)
            logging.debug('database connection initializing in vol-2')
            engine = create_engine("mysql+pymysql://root@localhost/drdo")
            logging.debug('database connected successfully for ',engine)
            engine.connect()
            df = pd.DataFrame({'company': [Company], 'country': [Country],'section':[Section],'general_title':[toc],'date':[date_conv],'status':[UpdateStatus],'filepath':[file_path],'SOURCE':[SOURCE],'TITLE':[title]})
            df.to_sql('hand2', engine, if_exists="replace")
            logging.debug('df ', df)
        #print(df)
        logging.warning('JANES HAND VOL 2 FILE SCRAPPINGS DONE HERE')
    except Exception as e:
        print(e)
        logging.exception('exception in vol 2 ', e)
    except OSError as filenotfoundex:
        print(filenotfoundex)
        logging.exception(' filenotfoundex exception in vol 2 ', filenotfoundex)
    except:
        pass
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        file_scrapping("F:/janesxml (1)/janesxml/data/yb/jnw/jnw2019/"+data_file)
        logging.exception('data_file in vol 2', data_file)
'''
def main(folder):
    number = count_files(folder)
    for data in range(number): '''

#file_scrapping('F:/janesxml (1)/janesxml/data/binder/jalw/jalw67/jalw2936.htm')
read_files("F:/janesxml (1)/janesxml/data/yb/jnw/jnw2019/")
logging.warning('read_files() in vol 2')



