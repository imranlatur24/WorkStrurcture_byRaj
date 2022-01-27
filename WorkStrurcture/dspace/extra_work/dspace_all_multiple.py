import os
import pandas as pd
import numpy as np
import mysql.connector
from flask import jsonify

#remove csv file or replace with newone
def remove_csv():
    os.system(
        r'cmd /c "C:\dspace\bin\dspace metadata-export -f C:\Users\3029\Documents\export\latescsv.csv --all"')

#remove existing data into dspace db before scrapping and insert new one
def remove_data():
    try:
        conn = sql_conn("localhost", "root", "", "testing")
        cursor= conn.cursor()
        cursor.execute("TRUNCATE TABLE `dspace`")
        data = cursor.fetchall()
        print('data in ',data)
        print('data type ',type(data))
        if data == 0:
            resp = jsonify('dspace database deleted successfully..')
        elif data != 0:
            resp = jsonify('dspace database deleted successfully..')
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
    return myconn

#csv to mysql db
def file_scrapping(file_path):
    #try:
    with open(file_path, encoding='cp437'):
        conn = sql_conn("localhost", "root", "", "testing")
        df_author = pd.read_csv(file_path,usecols=['dc.contributor.author[]'])#done
        df_author = df_author.fillna("")
        # for subject
        df_subject = pd.read_csv(file_path, usecols=['dc.subject[]'])#done
        df_subject_en_us = pd.read_csv(file_path, usecols=['dc.subject[en_US]'])

        # for description
        df_description = pd.read_csv(file_path, usecols=['dc.description[]'])#done
        df_description = df_description.fillna("")
        #df_description_en_us = pd.read_csv(file_path, usecols=['dc.description.abstract[en_US]'])


        # for date
        df_date_is = pd.read_csv(file_path, usecols=['dc.date.issued[]'])#done
        df_filepath = pd.read_csv(file_path, usecols=['dc.identifier.uri[]'])#done

        # for title
        df_title = pd.read_csv(file_path, usecols=['dc.title[]'])#done
        df_title_is = pd.read_csv(file_path, usecols=['dc.title[en_US]'])#done

        # convert df to df list array
        df_author_list = df_author.values.tolist()
        #for title
        df_title_list = df_title.values.tolist()
        df_title_is_list = df_title_is.values.tolist()

        #for date
        df_date_is_list = df_date_is.values.tolist()
        df_filepath_is_list = df_filepath.values.tolist()

        #for subject
        df_subject_list = df_subject.values.tolist()
        df_subject_en_us_list = df_subject_en_us.values.tolist()

        #for description
        df_description_list = df_description.values.tolist()
        #df_description_en_us_list = df_description_en_us.values.tolist()

        # convert df array to np array
        list_author = np.array(df_author_list)
        list_subject_en_us = np.array(df_subject_en_us_list)
        # for subject
        list_subject = np.array(df_subject_list)
        # for subject
        list_title_en_us = np.array(df_title_is_list)
        list_title = np.array(df_title_list)
        # for date
        list_date_is = np.array(df_date_is_list)
        list_filepath_is = np.array(df_filepath_is_list)
        # for description
        #list_description_en_us = np.array(df_description_en_us_list)
        list_description = np.array(df_description_list)

        # Multiplying arrays
        result_df_author = list_author.ravel()
        # for title
        result_df_title = list_title.ravel()
        result_df_title_is = list_title_en_us.ravel()

        # for date
        result_df_date_is = list_date_is.ravel()
        result_df_filepath_is = list_filepath_is.ravel()

        # for subject
        result_df_subject = list_subject.ravel()
        result_df_subject_en_us = list_subject_en_us.ravel()

        # for description
        result_df_description = list_description.ravel()
        #result_df_description_en_us = list_description_en_us.ravel()

        # convert nparray to normal arraylist
        df_author_arr = list(result_df_author)
        df_subject_arr = list(result_df_subject)
        # for date
        df_title_arr = list(result_df_title)
        df_title_is_arr = list(result_df_title_is)

        # for date
        df_date_is_arr = list(result_df_date_is)
        df_filepathis_arr = list(result_df_filepath_is)

        # for subject
        df_subject_en_us_arr = list(result_df_subject_en_us)

        # for description
        df_description_arr = list(result_df_description)
        #df_description_en_us_arr = list(result_df_description_en_us)

        # append second array list to first array list
        print('df_author_arr len ',len(df_author_arr))
        #for x in df_author_arr:
        #    df_author_arr.append(x)
        # for subject
        for x in df_subject_en_us_arr:
            df_subject_arr.append(x)
        # for description
        #for x in df_description_en_us_arr:
        #    df_description_arr.append(x)

        '''for x in df_date_is_arr:
            df_date_arr.append(x)'''
        for x in df_title_is_arr:
            df_title_arr.append(x)
        print('merge list df_title_arr ',df_title_arr)

        # creating emptry array for storing available value only for author
        author_arr = []
        subject_arr = []
        description_arr = []
        title_arr = []
        date_arr = []
        filepath_arr = []
        for row in df_author_arr: #values without duplicates 336 result found
            values = row
            author_arr.append(values)

        '''for i in df_author_arr:  # values with duplicates 76
            if i not in author_arr:
                author_arr.append(i)'''

        print('author scrapping started! ')
        print('result author! ', author_arr)
        print('length len! ', len(author_arr))

        for row in df_subject_arr: #values without duplicates 440 result found
            values = row
            if values == 'nan':
                print('')
            else:
                subject_arr.append(values)
        '''for i in df_subject_arr:  # values with duplicates 76
            if i not in subject_arr:
                subject_arr.append(i)'''

        print('subject scrapping started! ')
        print('result subject ! ', subject_arr)
        print('length len! ', len(subject_arr))

        for row in df_description_arr: #values without duplicates 440 result found
            values = row
            '''if values == 'nan':
                print('')
            else:'''
            description_arr.append(values)
        '''for i in df_description_arr:  # values with duplicates 76
            if i not in description_arr:
                description_arr.append(i)'''

        print('description scrapping started! ')
        print('result description ! ', description_arr)
        print('length len! ', len(description_arr))

        for row in df_date_is_arr: #values without duplicates 440 result found
            values = row
            if values == 'nan':
                print('')
            else:
                date_arr.append(values)
        '''for i in df_publisher_arr:  # values with duplicates 76
            if i not in publisher_arr:
                publisher_arr.append(i)'''

        print('date scrapping started! ')
        print('result date ! ', date_arr)
        print('length len! ', len(date_arr))


        for row in df_title_arr: #values without duplicates 440 result found
            values = row
            if values == 'nan':
                print('')
            else:
                title_arr.append(values)
        '''for i in df_publisher_arr:  # values with duplicates 76
            if i not in publisher_arr:
                publisher_arr.append(i)'''

        print('title scrapping started! ')
        print('result title ! ', title_arr)
        print('length len! ', len(title_arr))


        for row in df_filepathis_arr: #values without duplicates 440 result found
            values = row
            #print('filepth ',row)
            #if values == 'nan':
            #    print('')
            #else:
            filepath_arr.append(values)
        '''for i in df_publisher_arr:  # values with duplicates 76
            if i not in publisher_arr:
                publisher_arr.append(i)'''

        print('filepath scrapping started! ')
        print('result filepath ! ', filepath_arr)
        print('length len! ', len(filepath_arr))

        '''print('subject ', subject_arr)
        print('subject len ', len(subject_arr))
        print('publisher ', publisher_arr)
        print('publisher len ', len(publisher_arr))
        print('author ', author_arr)
        print('author len ', len(author_arr))
        print('description ', description_arr)
        print('description len ', len(description_arr))'''
        # creating the cursor object
        cur = conn.cursor()
        num = 0
        SOURCE='dspace'

        for i in author_arr:
            author = str(i)
            print('author ',author)
            sql = "INSERT INTO dspace VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ("", author, "", "", "", "", "", "", "")
            num = num + 1
            cur.execute(sql, val)
            #print('record inserted by dc_author')
            conn.commit()
        print('value of i', i)

        i = 1
        for title_i in title_arr:
            title = str(title_i)
            print('title ', title)
            sql = "UPDATE dspace SET TITLE=%s where id=%s"
            val = (title, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()
        print('value of i', i)

        i = 1
        for filepath_i in filepath_arr:
            filepath_l = str(filepath_i)
            print('filepath_l ', filepath_l)
            sql = "UPDATE dspace SET filepath=%s where id=%s"
            val = (filepath_l, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()
        print('value of i', i)




        i = 1
        for date_i in date_arr:
            date = str(date_i)
            print('date ', date)
            sql = "UPDATE dspace SET date_issued=%s where id=%s"
            val = (date, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()

        i = 1
        for description_arr_i in description_arr:
            desc = str(description_arr_i)
            print('description ', desc)
            sql = "UPDATE dspace SET DESCRIPTION=%s where id=%s"
            val = (desc, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()

        print('value of i', i)
        i = 1
        for subject_i in subject_arr:
            subject = str(subject_i)
            print('subject ', subject)
            sql = "UPDATE dspace SET subject=%s where id=%s"
            val = (subject, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()

        cur.execute('SELECT id FROM dspace ORDER BY id DESC LIMIT 1')
        limit_lectname = cur.fetchone()
        count = limit_lectname[0]
        str_count = str(count)
        print('total count ', str_count)

        i = 1
        for count_i in range(1, (count + 1)):
            print('source ', count_i)
            sql = "UPDATE dspace SET SOURCE=%s where id=%s"
            val = (SOURCE, i)
            num = num + 1
            i = i + 1
            cur.execute(sql, val)
            # print('record inserted by dc_title[]')
            conn.commit()


    #except:
    #    pass

def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])

def read_files(folder_path):
    for data_file in sorted(os.listdir(folder_path)):
        file_scrapping("C:/Users/3029/Documents/export/"+data_file)

remove_csv()
remove_data()
read_files("C:/Users/3029/Documents/export")
