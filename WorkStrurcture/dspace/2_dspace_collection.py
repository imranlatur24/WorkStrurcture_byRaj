# https://stackoverflow.com/questions/4685173/delete-all-duplicate-rows-except-for-one-in-mysql
# how to read file from ip address using python code in windows

import os
import pandas as pd
from sqlalchemy import create_engine
import logging

engine = create_engine("mysql+pymysql://root@localhost/testing")
engine.connect()
def file_scrapping(file_path):
    try:
        with open(file_path, encoding='cp437'):
            print(file_path)
            col_list = ['dc.contributor.author[]', 'dc.date.issued[]', 'dc.identifier.uri',
                         'dc.title[]']
            df = pd.read_csv(file_path, usecols=col_list)  # done
            df.drop(index=df.index[0],
                    axis=0,
                    inplace=True)

            df.rename(columns={'dc.contributor.author[]': 'author',
                               'dc.date.issued[]': 'date_issued',
                               'dc.description[]': 'DESCRIPTION',
                               'dc.identifier.uri': 'filepath',
                               'dc.title[]': 'TITLE',
                               }, inplace=True)
            print(df)
            df.to_sql(name='dspace', con=engine, if_exists='replace',index=False)
    except Exception as e:
        print(e)
        logging.exception('exception in vol 2 ', e)
    except:
        pass


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])

def read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        file_scrapping("C:/Users/rtatt/Downloads/Compressed/collections-20210703T095546Z-001/collections/"+data_file)

read_files("C:/Users/rtatt/Downloads/Compressed/collections-20210703T095546Z-001/collections/")
