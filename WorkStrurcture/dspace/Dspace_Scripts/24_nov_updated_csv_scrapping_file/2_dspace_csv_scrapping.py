import os
import pandas as pd
from pandas import DataFrame
import mysql.connector
from flask import jsonify
from sqlalchemy import create_engine
from datetime import datetime
import logging
from sqlalchemy.exc import IntegrityError
logging.basicConfig(
    #filename = logging.FileHandler('E:/DRDO/ALL API/log.log'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S_%f'))),
    filename = datetime.now().strftime('DSPACE_Community_23_%d-%b-%Y.log'),
    #filename='E:/DRDO/all_project/all_project/drdo.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
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
dbname = "testing"
#remove existing data into dspace db before scrapping and insert new one
def remove_data():
    try:
        conn = sql_conn("localhost", "root", "", dbname)
        cursor= conn.cursor()
        cursor.execute("TRUNCATE TABLE `dspace`")
        data = cursor.fetchall()
        print('data in ',data)
        if data == 0:
            # logging.debug('dspace database deleted successfully..')
            resp = jsonify('dspace database deleted successfully..if')
        elif data != 0:
            resp = jsonify('dspace database deleted successfully..')
            # logging.debug('dspace database deleted successfully..elif')
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
#creating connection with testing db
def sql_conn(hostname,username,password,dbname):
    myconn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname)
    print('connected successfully')
    logging.info('connected succesfully in 2_dpsace_merge_completed file')
    logging.debug('myconn data ',myconn)
    return myconn
###################################################
engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
########################################### collection_14_16_19_20_create_csv ############################################################################
filepath_14_16_19_20 = "E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/Collections/"
#remove existing data into dspace db before scrapping and insert new one
def collection_14_16_19_20_create_csv(file_path,data_file):
        with open(file_path, encoding='cp437'):
            print('data_file == ',data_file)
            col_list = ['id','dc.contributor.author[]', 'dc.date.issued[]', 'dc.identifier.uri',
                        'dc.description.provenance[en]', 'dc.title[]','dc.title[en_US]']
            logging.info('dspace col_list in collection ', col_list)
            logging.info('dspace data file  ', data_file)
            # if col isnot avaible then csv will created https://stackoverflow.com/questions/63002350/ignore-missing-columns-in-usecol-parameter
            df1 = pd.read_csv(file_path, low_memory=False, usecols=lambda x: x in col_list)
            col_list2 = ['dc.title[]','dc.title[en_US]']
            df2 = pd.read_csv(file_path, low_memory=False, usecols=col_list2)  # done
            logging.info('dspace col_list in collection ', df2)
            print('\n')
            #fillna is used for replace  NaN with "" black spaces
            df2['MyTitle'] = df2['dc.title[]'].fillna("").map(str) + '' + df2['dc.title[en_US]'].fillna("").map(str)
            # print(df1)
            # print(df2['MyTitle'])
            # print(df1.merge(df2))
            df3=df1.merge(df2)
            #remove duplication by uri cols
            #https://stackoverflow.com/questions/50982727/using-duplicates-values-from-one-column-to-remove-entire-row-in-pandas-dataframe
            df3 = df3.drop_duplicates(subset=['dc.identifier.uri'], keep='first')
            df3.to_csv("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/collection_csv_new_mytitle/"+data_file)
            print(df3)
        # df3.to_sql(name='dspace', con=engine, if_exists='append',index=False)
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def collection_14_16_19_20_read_files(folder_path):
    for data_file_collection in sorted(os.listdir(folder_path)):
        collection_14_16_19_20_create_csv(filepath_14_16_19_20 + data_file_collection,data_file_collection)
remove_data()
collection_14_16_19_20_read_files(filepath_14_16_19_20)

########################################### collection_14_16_19_20_SQL #####################################################################
def collection_14_16_19_20_SQL(data_file_db):
    try:
        with open(data_file_db, encoding='cp437'):
            print(data_file_db)
            logging.info('dspace filepath', data_file_db)
            col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.description.provenance[en]','dc.identifier.uri','MyTitle']
            print(col_list)
            logging.info('collection no ',data_file_db," headers are ",col_list)
            logging.info('dspace col_list in collection ', col_list)
            df = pd.read_csv(data_file_db,low_memory=False,usecols=col_list)#done
            print(df)
            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]':'date_issued',
                               'dc.description.provenance[en]':'DESCRIPTION',
                               'dc.identifier.uri': 'filepath',
                               'MyTitle': 'TITLE',
                               }, inplace=True)
            # print(df)
            # logging.info('dpsace col rename ', df)
            df.to_sql(name='dspace', con=engine, if_exists='append',index=False)
    except IntegrityError as ie:
        print("Duplicate key found. Exiting.",ie)
        pass
def collection_14_16_19_20_read_files(folder_path):
    for data_file_db in sorted(os.listdir(folder_path)):
        collection_14_16_19_20_SQL("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/collection_csv_new_mytitle/" + data_file_db)
collection_14_16_19_20_read_files("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/collection_csv_new_mytitle/")

################################################ community_1_3_30_34_create_csv ########################################################################
filepath_Community_1_3_30_34 = "E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/Community/"
def community_1_3_30_34_create_csv(file_path, data_file):
    with open(file_path, encoding='cp437'):
        print('data_file == ', data_file)
        col_list = ['id', 'dc.contributor.author[]', 'dc.date.issued[]', 'dc.identifier.uri',
                    'dc.description.provenance[en]', 'dc.title[]', 'dc.title[en_US]']
        logging.info('community no ',data_file," headers are ",col_list)
        # if col isnot avaible then csv will created https://stackoverflow.com/questions/63002350/ignore-missing-columns-in-usecol-parameter
        df1 = pd.read_csv(file_path, low_memory=False, usecols=lambda x: x in col_list)
        col_list2 = ['dc.title[]', 'dc.title[en_US]']
        df2 = pd.read_csv(file_path, low_memory=False, usecols=col_list2)  # done
        logging.info('dspace col_list in collection ', df2)
        print('\n')
        # fillna is used for replace  NaN with "" black spaces
        df2['MyTitle'] = df2['dc.title[]'].fillna("").map(str) + '' + df2['dc.title[en_US]'].fillna("").map(str)
        # print(df1)
        # print(df2['MyTitle'])
        # print(df1.merge(df2))
        df3 = df1.merge(df2)
        # remove duplication by uri cols
        # https://stackoverflow.com/questions/50982727/using-duplicates-values-from-one-column-to-remove-entire-row-in-pandas-dataframe
        df3 = df3.drop_duplicates(subset=['dc.identifier.uri'], keep='first')
        df3.to_csv("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/community_csv_new_mytitle/" + data_file)
        print(df3)
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def community_1_3_30_34_read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        community_1_3_30_34_create_csv(filepath_Community_1_3_30_34 + data_file,data_file)
community_1_3_30_34_read_files(filepath_Community_1_3_30_34)

########################################### community_1_3_30_34_SQL #####################################################################
def community_1_3_30_34__SQL(commdata_file_db):
    try:
        with open(commdata_file_db, encoding='cp437'):
            print(commdata_file_db)
            logging.info('dspace filepath', commdata_file_db)
            col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.description.provenance[en]','dc.identifier.uri','MyTitle']
            print(col_list)
            logging.info('community no ',commdata_file_db," headers are ",col_list)
            logging.info('dspace col_list in collection ', col_list)
            df = pd.read_csv(commdata_file_db,low_memory=False,usecols=col_list)#done
            print(df)
            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]':'date_issued',
                               'dc.description.provenance[en]':'DESCRIPTION',
                               'dc.identifier.uri': 'filepath',
                               'MyTitle': 'TITLE',
                               }, inplace=True)
            df.to_sql(name='dspace', con=engine, if_exists='append',index=False)
    except IntegrityError as ie:
        print("Duplicate key found. Exiting.",ie)
        pass
def community_1_3_30_34__SQL_read_files(folder_path):
    for commdata_file_db in sorted(os.listdir(folder_path)):
        community_1_3_30_34__SQL("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/community_csv_new_mytitle/" + commdata_file_db)
community_1_3_30_34__SQL_read_files("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/community_csv_new_mytitle/")

################################################## community 23 create_csv ##################################################
filepath_23 = "E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/23/"
#remove existing data into dspace db before scrapping and insert new one
def community_23(file_path,data_file):
        with open(file_path, encoding='cp437'):
            print('data_file == ',data_file)
            col_list = ['dc.contributor.author[]', 'dc.date.issued[]', 'dc.identifier.issn[]',
                        'dc.description.provenance[en]','dc.title.alternative[en_US]',
                        'dc.title[]', 'dc.subject[]', 'dc.publisher[]']
            logging.info('dspace col_list in community 23 ', col_list)
            logging.info('dspace data file  ', data_file)
            # if col isnot avaible then csv will created https://stackoverflow.com/questions/63002350/ignore-missing-columns-in-usecol-parameter
            df1 = pd.read_csv(file_path, low_memory=False, usecols=lambda x: x in col_list)
            col_list2 = ['dc.title[]','dc.title.alternative[en_US]']
            df2 = pd.read_csv(file_path, low_memory=False, usecols=col_list2)  # done
            logging.info('dspace col_list in community 23 ', df2)
            print('\n')
            #fillna is used for replace  NaN with "" black spaces
            df2['MyTitle'] = df2['dc.title[]'].fillna("").map(str) + '' + df2['dc.title.alternative[en_US]'].fillna("").map(str)
            # print(df1)
            # print(df2['MyTitle'])
            # print(df1.merge(df2))
            df3=df1.merge(df2)
            df3 = df3.drop_duplicates(subset=['dc.identifier.issn[]'], keep='first')
            df3.to_csv("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/23_community_csv_new_mytitle/"+data_file)
            # print(df3)
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def community_23_read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        community_23(filepath_23 + data_file,data_file)
community_23_read_files(filepath_23)

################################################## insert to sql 23 community to sql ##################################################
def community_23_sql(file_path):
    try:
        with open(file_path, encoding='cp437'):
            print(file_path)
            col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.identifier.issn[]',
                        'dc.description.provenance[en]','MyTitle','dc.subject[]','dc.publisher[]']
            df = pd.read_csv(file_path,low_memory=False,usecols=col_list)#done
            logging.info('community no ',file_path," headers are ",col_list)
            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]':'date_issued',
                               'dc.description.provenance[en]':'DESCRIPTION',
                               'dc.identifier.issn[]': 'filepath',
                               'MyTitle': 'TITLE',
                               'dc.subject[]': 'subject',
                               'dc.publisher[]': 'publisher',
                               }, inplace=True)
            print(df)
            df.to_sql(name='dspace', con=engine, if_exists='append',index=False)
    except:
        pass
def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
def community_23_sql_read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        community_23_sql("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/23_community_csv_new_mytitle/" + data_file)
community_23_sql_read_files("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace/23_community_csv_new_mytitle/")

################################################## insert 32 en to sql ##################################################
# def community_32_sql(file_path):
#     try:
#         with open(file_path, encoding='cp437'):
#             print(file_path)
#             col_list = ['dc.contributor.author[]','dc.date.issued[]','dc.identifier.uri',
#                         'dc.description.provenance[en]','dc.title[]','dc.subject[]','dc.publisher[]']
#             logging.info('community no ',file_path," headers are ",col_list)
#             df = pd.read_csv(file_path, low_memory=False,usecols=col_list)#done
#             df = df.drop_duplicates(subset=['dc.identifier.uri'], keep='first')
#             df.rename(columns={'dc.contributor.author[]': 'author',
#                                'dc.date.issued[]':'date_issued',
#                                'dc.description.provenance[en]':'DESCRIPTION',
#                                'dc.identifier.uri': 'filepath',
#                                'dc.title[]': 'TITLE',
#                                'dc.subject[]': 'subject',
#                                'dc.publisher[]': 'publisher',
#                                }, inplace=True)
#             print(df)
#             df.to_sql(name='dspace', con=engine, if_exists='append',index=False)
#     except:
#         pass
# def count_files(dir):
#     return len([1 for x in list(os.scandir(dir)) if x.is_file()])
# def community_32_sql_read_files(folder_path):
#     for data_file in sorted(os.listdir(folder_path)):
#         community_32_sql("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace_15_nove_troubleshooting/32/" + data_file)
# community_32_sql_read_files("E:/WorkStrurcture_byRaj/WorkStrurcture/dspace_15_nove_troubleshooting/32/")
