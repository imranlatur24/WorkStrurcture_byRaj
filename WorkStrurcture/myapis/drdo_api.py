import difflib
import re
import smtplib
from email.mime.text import MIMEText
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
from flask_restful import reqparse
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import logging
import random
import string
from autocorrect import Speller

# app=Flask(__name__)
# CORS(app,support_credential=True)
# cross_origin(app, support_credential=True)

# for janes filter api variable
csearch = ''
status_db = []
section_db = []
country_db = []
general_title_db = []
# for nptel filter api global variable
institute_db = []
filetype_db = []
coordinators_db = []
subjectName_db = []
disciplineName_db = []
#for dspace
subject_db = []
author_db = []
date_issued_db = []
logging.basicConfig(
    filename='C:/wamp64/www/build/WorkStrurcture_30JUNE/WorkStrurcture/WorkStrurcture/logs/apis_report.log',
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
logging.info('FINAL FILTERS FILE CALLING FOR APIS')
logging.info('database connection initializing')
# from register_drdo_db import mysql
app = Flask(__name__)
CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testing'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
# logging.exception(mysql)
logging.info('database connection established')
closematch=''
#common db ########################################################################################################################################
def closeMatches(patterns, word):
    return difflib.get_close_matches(word, patterns, n=10, cutoff=0.3)

def closeMatches2(patterns):
    return patterns
#common db ########################################################################################################################################
#common db ########################################################################################################################################
@app.route('/common_db', methods=['GET'])
def get_user():
    conn = None
    cursor = None
    try:
        mydictionary_common_db = {}
        mydictionary_common_db["common_db"] = []
        common_db = mydictionary_common_db["common_db"]
        csearch = request.args.get('q')
        types = request.args.get('types')
        # print(types)
        # csearch = 'introduction of'
        combine_arr = {**mydictionary_common_db}
        arr_list = []
        janes_country = []
        my_dict = {}
        print('types ', types)
        logging.info('#User search string : ', csearch)
        print('# user search ', csearch)
        if csearch:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            if types == 'ALL':
                cursor.execute(
                    "(select * from child_real where TITLE LIKE\"%" + csearch + "%\") UNION ALL (select * from child_real where coordinators LIKE \"%" + csearch + "%\") UNION ALL (select * from child_real where Institute LIKE \"%" + csearch + "%\") UNION ALL (select * from child_real where disciplineName LIKE \"%" + csearch + "%\") UNION ALL (select * from child_real where subjectName LIKE \"%" + csearch + "%\")")
                logging.info('NPTEL SQL Query executing')
                child_real_rows = cursor.fetchall()
                for row in child_real_rows:
                    common_db.append(row)
                    logging.info('appending NPTEL data to nptel Array', row)

                cursor.execute(
                    "(select * from hand where TITLE LIKE\"%" + csearch + "%\") UNION ALL (select * from hand where company LIKE \"%" + csearch + "%\") UNION ALL (select * from hand where section LIKE \"%" + csearch + "%\") UNION ALL (select * from hand where general_title LIKE \"%" + csearch + "%\")")
                logging.info('Janes Handbook SQL Query executing')
                hand_janes = cursor.fetchall()
                for jrow in hand_janes:
                    common_db.append(jrow)
                    logging.info('appending James Handbook data to janes Array', jrow)

                cursor.execute("select * from libsys WHERE TITLE LIKE %s", ("%" + csearch + "%",))
                logging.info('LIBSYS SQL Query executing')
                lib = cursor.fetchall()
                for jrow in lib:
                    common_db.append(jrow)
                    logging.info('appending LIBSYS data to libsys Array', jrow)

                cursor.execute(
                    "select * from armablog_filepath WHERE TITLE LIKE %s", ("%" + csearch + "%",))
                logging.info('ARMABLOG SQL Query executing')
                wp_comments_janes = cursor.fetchall()
                for jrow in wp_comments_janes:
                    common_db.append(jrow)
                    logging.info('appending ARMABLOG data to arma Array', jrow)

                cursor.execute(
                    "(select * from dspace where TITLE LIKE\"%" + csearch + "%\") UNION ALL (select * from dspace where author LIKE \"%" + csearch + "%\") UNION ALL (select * from dspace where DESCRIPTION LIKE \"%" + csearch + "%\") UNION ALL (select * from dspace where subject LIKE \"%" + csearch + "%\")")
                logging.info('dspace SQL Query executing')
                metadatavalue_janes = cursor.fetchall()
                for jrow in metadatavalue_janes:
                    common_db.append(jrow)
                    logging.info('appending dspace data to dspace Array', jrow)
                    logging.info(
                        'Creating dictionary using nptel,arma,libsys,janes,dspace')

            elif types == 'NPTEL':
                cursor.execute(
                    "(select * from child_real where TITLE LIKE\"%" + csearch + "%\")")
                    # UNION ALL (select * from child_real where coordinators LIKE \"%" +
                    # coordinators_db + "%\") UNION ALL (select * from child_real where Institute LIKE \"%" +
                    # institute_db + "%\") UNION ALL (select * from child_real where disciplineName LIKE \"%" +
                    # disciplineName_db + "%\") UNION ALL (select * from child_real where subjectName LIKE \"%" +
                    # subjectName_db + "%\")")
                logging.info('NPTEL SQL Query executing')
                child_real_rows = cursor.fetchall()
                for row in child_real_rows:
                    common_db.append(row)
                    institute_db.append(row['Institute'])
                    filetype_db.append(row['filetype'])
                    coordinators_db.append(row['coordinators'])
                    subjectName_db.append(row['subjectName'])
                    disciplineName_db.append(row['disciplineName'])

                    logging.info('appending NPTEL data to nptel Array', row)
                # print('institute here ', institute_db)
                # print('filetype here ', filetype_db)
                # print('coordinators here ', coordinators_db)
                # print('subjectName here ', subjectName_db)
                # print('disciplineName here ', disciplineName_db)

                # print(combine_arr)
                for i, j in combine_arr.items():
                    for x in j:
                        arr_list.append(x['TITLE'])

                        logging.info(
                            'Appending titles in array list based on csearch', x['TITLE'])

                my_dict['did_u_mean'] = closeMatches(list(set(arr_list)), csearch)

                logging.info('got did you mean results', my_dict['did_u_mean'])
                combine_arr.update(my_dict)

            elif types == 'JANES':
                # FOR AMMUNITION SEARCH
                # (SELECT * FROM `hand` WHERE title LIKE'%ammunition%') UNION ALL (SELECT * FROM `hand`WHERE company LIKE '%ammunition%') UNION ALL (SELECT * FROM `hand`WHERE section LIKE'%ammunition%') UNION ALL (SELECT * FROM hand WHERE general_title LIKE'%ammunition%');
                cursor.execute(
                    "(select * from hand where TITLE LIKE\"%" +csearch + "%\")")
                    # csearch + "%\") UNION ALL (select * from hand where company LIKE \"%" +
                    # csearch + "%\") UNION ALL (select * from hand where section LIKE \"%" +
                    # csearch + "%\") UNION ALL (select * from hand where general_title LIKE \"%" +
                    # csearch + "%\")")
                logging.info('Janes Handbook SQL Query executing')
                hand_janes = cursor.fetchall()
                for jrow in hand_janes:
                    common_db.append(jrow)
                    status_db.append(jrow['status'])
                    country_db.append(jrow['country'])
                    section_db.append(jrow['section'])
                    general_title_db.append(jrow['general_title'])
                    # for db in common_db:

                    # logging.info('appending James Handbook data to janes Array', jrow)
                '''print('status here ', status_db)
                print('country_db here ', country_db)
                print('section_db here ', section_db)
                print('general_title_db here ', general_title_db)'''
                for i, j in combine_arr.items():
                    for x in j:
                        arr_list.append(x['title'])
                        logging.info('Appending titles in array list based on csearch', x['title'])
                my_dict['did_u_mean'] = closeMatches(list(set(arr_list)), csearch)
                logging.info('got did you mean results', my_dict['did_u_mean'])
                combine_arr.update(my_dict)
                # print(type(combine_arr))
                # print('combine_arr',combine_arr)

            elif types == 'ARMA':
                cursor.execute(
                    "SELECT * FROM armablog_filepath WHERE TITLE LIKE %s", ("%" + csearch + "%",))
                logging.info('ARMABLOG SQL Query executing')
                print('armablog csearch ', csearch)
                wp_comments_janes = cursor.fetchall()
                for jrow in wp_comments_janes:
                    common_db.append(jrow)
                    logging.info('appending ARMABLOG data to arma Array', jrow)
                    # print(combine_arr)
                for i, j in combine_arr.items():
                    for x in j:
                        arr_list.append(x['TITLE'])
                        logging.info(
                            'Appending titles in array list based on csearch', x['TITLE'])

                my_dict['did_u_mean'] = closeMatches(
                    list(set(arr_list)), csearch)
                logging.info('got did you mean results', my_dict['did_u_mean'])
                combine_arr.update(my_dict)

            elif types == 'LIBSYS':
                # best match below 1 for intro keyword shows 761 for similar worlds like intro and introduction etc
                cursor.execute(
                    "select * from libsys WHERE TITLE LIKE %s", ("%" + csearch + "%",))

                '''cursor.execute(
                    "select * from libsys WHERE TITLE LIKE %s", ("%" + csearch + "%",))'''
                # logging.info('LIBSYS SQL Query executing')
                lib = cursor.fetchall()
                for jrow in lib:
                    common_db.append(jrow)
                    logging.info('appending LIBSYS data to libsys Array', jrow)
                logging.info('Janes Handbook SQL Query executing')
                for i, j in combine_arr.items():
                    for x in j:
                        arr_list.append(x['TITLE'])
                        logging.info(
                            'Appending titles in array list based on csearch', x['TITLE'])
                my_dict['did_u_mean'] = closeMatches(list(set(arr_list)), csearch)
                logging.info('got did you mean results', my_dict['did_u_mean'])
                combine_arr.update(my_dict)

            elif types == 'DSPACE':
                cursor.execute(
                    "(select * from dspace where TITLE LIKE\"%" +csearch + "%\")")
                    # csearch + "%\") UNION ALL (select * from dspace where author LIKE \"%" +
                    # csearch + "%\") UNION ALL (select * from dspace where DESCRIPTION LIKE \"%" +
                    # csearch + "%\") UNION ALL (select * from dspace where subject LIKE \"%" +
                    # csearch + "%\")")
                dspace = cursor.fetchall()
                for jrow in dspace:
                    common_db.append(jrow)
                    author_db.append(jrow['author'])
                    date_issued_db.append(jrow['date_issued'])
                    subject_db.append(jrow['subject'])
                    logging.info('appending dspace data to dspace Array', jrow)
                logging.info('dspace SQL Query executing')
                for i, j in combine_arr.items():
                    for x in j:
                        arr_list.append(x['TITLE'])
                        logging.info(
                            'Appending titles in array list based on csearch', x['TITLE'])
                my_dict['did_u_mean'] = closeMatches(list(set(arr_list)), csearch)
                logging.info('got did you mean results', my_dict['did_u_mean'])
                combine_arr.update(my_dict)

            resp = jsonify(combine_arr)
            logging.info('Successfully created JSON')
            resp.status_code = 200
            return resp

    except Exception as e:
        print(e)
        print('exception found in common_db')
    finally:
        cursor.close()
        conn.close()

# DSPACE FILTER WISE LIST
@app.route('/filter_wise_dspace', methods=['POST'])
def filter_wise_dspace():
    data = request.get_json()
    csearch = data['dsearch']
    author = data['author']
    subject = data['subject']
    date_issued = data['date_issued']
    print('dsearch', csearch)
    print('author ', author)
    print('subject', subject)
    print('date_issued', date_issued)
    mydictionary_dsapce = {}
    mydictionary_dsapce["common_db"] = []
    dspace = mydictionary_dsapce["common_db"]
    data1 = ''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if csearch == '0':
    #     cursor.execute(
    #         "select * from hand where date_issued NOT LIKE\"%" + csearch + "%\"")
    # if csearch == '-':
    #     cursor.execute(
    #         "select * from hand where date_issued NOT LIKE\"%" + csearch + "%\"")
    if csearch:
        cursor.execute(
            "SELECT * FROM `dspace` WHERE TITLE LIKE\"%" + csearch + "%\" AND author LIKE \"%" + author + "%\" AND subject LIKE \"%" + subject + "%\" AND date_issued LIKE\"%" + date_issued + "%\"")
        testing_rows = cursor.fetchall()
        for row in testing_rows:
            # data1 = row
            dspace.append(row)
            author_db.append(row['author'])
            date_issued_db.append(row['date_issued'])
            subject_db.append(row['subject'])
        combine_arr = {**mydictionary_dsapce}
        resp = jsonify(combine_arr)
        return resp

@app.route('/filter_wise_janes', methods=['POST'])
def filter_wise_janes():
    data = request.get_json()
    jsearch = data["csearch"]
    country = data["country"]
    section = data["section"]
    general_title = data["general_title"]
    status = data["status"]
    mydictionary_janes = {}
    mydictionary_janes["common_db"] = []
    janes = mydictionary_janes["common_db"]
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if jsearch:
        cursor.execute(
            "select * from hand where TITLE LIKE\"%" + jsearch + "%\" AND country LIKE \"%" + country + "%\" AND section LIKE \"%" + section + "%\" AND general_title LIKE\"%" + general_title + "%\" AND status LIKE \"%" + status + "%\"")
        testing_rows = cursor.fetchall()
        print('total count ', len(testing_rows))
        print('testing_rows inside regrex block ', testing_rows)
        for row in testing_rows:
            # print('test', row)
            janes.append(row)
            status_db.append(row['status'])
            country_db.append(row['country'])
            section_db.append(row['section'])
            general_title_db.append(row['general_title'])
        combine_arr = {**mydictionary_janes}
        resp = jsonify(combine_arr)
        return resp

@app.route('/filter_wise_nptel', methods=['POST'])
def filter_wise_nptel():
    data = request.get_json()
    csearch = data["csearch"]
    print(csearch)
    filetype = data["filetype"]
    disciplineName = data["disciplineName"]
    subjectName = data["subjectName"]
    institute = data["institute"]
    coordinator = data["coordinator"]
    mydictionary_nptel = {}
    mydictionary_nptel["common_db"] = []
    nptel = mydictionary_nptel["common_db"]
    data1 = ''
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if csearch:
        cursor.execute(
            "SELECT * FROM `child_real` WHERE TITLE LIKE\"%" + csearch + "%\" AND disciplineName LIKE \"%" + disciplineName + "%\" AND subjectName LIKE \"%" + subjectName + "%\" AND Institute LIKE\"%" + institute + "%\" AND filetype LIKE \"%" + filetype + "%\" AND coordinators LIKE \"%" + coordinator + "%\"")
        testing_rows = cursor.fetchall()
        my_list = list(testing_rows)
        print('count nptel ',len(my_list))
        #print('mylist type ', type(my_list))
        for row in my_list:
            nptel.append(row)
            institute_db.append(row['Institute'])
            filetype_db.append(row['filetype'])
            coordinators_db.append(row['coordinators'])
            subjectName_db.append(row['subjectName'])
            disciplineName_db.append(row['disciplineName'])
            # we required one hit for all the filter as well as reset all button right side on top corner
        # nptel_data_arr = nptel_arr
        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        return resp

@app.route('/author', methods=['GET'])
def get_author():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["author"] = []
        res = mydictionary_res["author"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = author_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('institute_db global', author_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('author_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"author": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in author_db', 500)
            return resp
        else:
            resp = jsonify('no author_db found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear author data
        author_db.clear()
        cursor.close()
        conn.close()

@app.route('/date_issued', methods=['GET'])
def get_date_issued():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["date_issued"] = []
        res = mydictionary_res["date_issued"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = date_issued_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('date_issued_db global', date_issued_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('date_issued_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"date_issued": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in date_issued_db', 500)
            return resp
        else:
            resp = jsonify('no date_issued_db found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear author data
        date_issued_db.clear()
        cursor.close()
        conn.close()

@app.route('/subject', methods=['GET'])
def get_subject():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["subject"] = []
        res = mydictionary_res["subject"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = subject_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('subject_db global', subject_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('subject_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"subject": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in subject_db', 500)
            return resp
        else:
            resp = jsonify('no subject_db found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear subject data
        subject_db.clear()
        cursor.close()
        conn.close()

@app.route('/autocompleteview_dspace', methods=['GET'])
def get_autocomplete_dspace():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_dspace"] = []
        nptel = mydictionary_nptel["autocompleteview_dspace"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select DISTINCT(TITLE) FROM `dspace_merge` ORDER BY TITLE")
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found in autocompleteview_dspace')
    finally:
        cursor.close()
        conn.close()

@app.route('/autocompleteview_all', methods=['GET'])
def get_autocomplete_all():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_all"] = []
        nptel = mydictionary_nptel["autocompleteview_all"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #cursor.execute("select DISTINCT(TITLE) FROM `all_merge` ORDER BY TITLE")
        cursor.execute("select DISTINCT(TITLE) from dspace where TITLE LIKE\"%" + csearch + "%\"")
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found in autocompleteview_all')
    finally:
        cursor.close()
        conn.close()

@app.route('/sort_by_title', methods=['GET'])
def get_sort_by_title():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["sort_by_title"] = []
        nptel = mydictionary_nptel["sort_by_title"]
        types = request.args.get('types')
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # ARMABLOG
        if types == "ALL":
            print("value", types)
            cursor.execute(
                "select * from armablog_filepath ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
        # JANES
            cursor.execute(
                "select * from hand ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
        # LIBSYS
            cursor.execute(
                "select * from libsys ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
        # NPTEL
            cursor.execute(
                "select * from child_real ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
        # DSPACE
            cursor.execute(
                "SELECT * FROM dspace ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)

            combine_arr = {**mydictionary_nptel}
            print("result", nptel)
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

        elif types == 'ARMA':
            cursor.execute(
                "select * from armablog_filepath ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
            combine_arr = {**mydictionary_nptel}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

        elif types == 'JANES':
            cursor.execute(
                "select * from hand ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
            combine_arr = {**mydictionary_nptel}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

        elif types == 'LIBSYS':
            cursor.execute(
                "select * from libsys ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
            combine_arr = {**mydictionary_nptel}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

        elif types == 'NPTEL':
            cursor.execute(
                "select * from child_real ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
            combine_arr = {**mydictionary_nptel}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

        elif types == 'DSPACE':
            cursor.execute(
                "select * from dspace ORDER BY TITLE")
            wp_comments_nptel = cursor.fetchall()
            for jrow in wp_comments_nptel:
                nptel.append(jrow)
            combine_arr = {**mydictionary_nptel}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

    except Exception as e:
        print(e)
        print('exception found sort_by_title')
    finally:
        cursor.close()
        conn.close()

@app.route('/autocompleteview_janes', methods=['GET'])
def get_autocomplete_janes():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_janes"] = []
        nptel = mydictionary_nptel["autocompleteview_janes"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT TITLE FROM janes_merge ORDER BY TITLE * 1, TITLE ASC")
        #cursor.execute("SELECT TITLE  from all_merge ORDER BY (TITLE +0) ASC ,TITLE ASC")
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}

        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found autocompleteview_janes')
    finally:
        cursor.close()
        conn.close()


@app.route('/autocompleteview_arma', methods=['GET'])
def get_autocomplete_view1():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_arma"] = []
        nptel = mydictionary_nptel["autocompleteview_arma"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        '''cursor.execute(
            "select DISTINCT(TITLE) from armablog_filepath ORDER BY TITLE")'''
        cursor.execute(
            "SELECT TITLE, TRIM(LEADING 'New Post Published -' FROM TITLE) FROM armablog_filepath")
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found in autocompleteview_arma')
    finally:
        cursor.close()
        conn.close()


@app.route('/autocompleteview_nptl', methods=['GET'])
def get_autocomplete_view2():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_nptl"] = []
        nptel = mydictionary_nptel["autocompleteview_nptl"]
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('select DISTINCT(TITLE) from nptel_merge ORDER BY TITLE')
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)
            #print('nptel_merge auto ',jrow)
        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        print('exception found in autocompleteview_nptl')
    finally:
        cursor.close()
        conn.close()


@app.route('/autocompleteview_libsys', methods=['GET'])
def get_autocomplete_view3():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocompleteview_libsys"] = []
        nptel = mydictionary_nptel["autocompleteview_libsys"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "select DISTINCT(TITLE) from libsys ORDER BY TITLE")
        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found autocompleteview_libsys')
    finally:
        cursor.close()
        conn.close()


@app.route('/autocomplete_view', methods=['GET'])
def get_autocomplete_view_comman():
    conn = None
    cursor = None
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["autocomplete_view"] = []
        nptel = mydictionary_nptel["autocomplete_view"]
        # dspace_cur = dconn.cursor()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #cursor.execute("select DISTINCT(TITLE) from all_merge where TITLE LIKE\"%" + csearch + "%\"ORDER BY TITLE")
        cursor.execute("SELECT TITLE FROM all_merge ORDER BY TITLE * 1, TITLE ASC")


        wp_comments_janes = cursor.fetchall()
        for jrow in wp_comments_janes:
            nptel.append(jrow)

        combine_arr = {**mydictionary_nptel}
        resp = jsonify(combine_arr)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('exception found autocompleteview_all')
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_by_single_notification', methods=['POST'])
def get_delete_by_single_notification():
    data = request.get_json()
    print(data)
    id = data['id']
    print('delete id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
    sql = "DELETE FROM `usr_notification` WHERE id=%s"
    values = id
    cursor.execute(sql, values)
    conn.commit()
    resp = jsonify(message='record removed from notifications successfully')
    resp.status_code = 200
    return resp

@app.route('/delete_by_all_notification', methods=['POST'])
def get_delete_by_all_library():
    data = request.get_json()
    print(data)
    id = data['EmpID']
    print('delete id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "DELETE FROM `usr_notification` WHERE EmpID=%s"
    values = id
    cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
    cursor.execute(sql, values)
    conn.commit()
    resp = jsonify(message='All notifications deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/delete_by_single_library', methods=['POST'])
def get_delete_by_single_library():
    data = request.get_json()
    print(data)
    id = data['id']
    print('delete id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "DELETE FROM `usr_fav` WHERE id=%s"
    values = id
    cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
    cursor.execute(sql, values)
    conn.commit()
    resp = jsonify(message='record removed from favourite successfully')
    resp.status_code = 200
    return resp

@cross_origin()
@app.route('/usr_search_history', methods=['POST'])
def get_usr_search_history():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    search_history = data['search_history']
    #filepath = data['filepath']
    mark = data['mark']
    #source = data['source']
    print('EmpID', EmpID)
    print('EmpID type', type(EmpID))
    print('search history', search_history)
    #print('filepath', filepath)
    print('mark', mark)
    #print('source', source)
    id_match = ''
    search_hist_match = ''
    source_ = ''
    try:
        sql = "SELECT * FROM `usr_search_history` WHERE EmpID=%s and search_history=%s"
        values = (EmpID, search_history)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
        cursor.execute(sql, values)
        result = cursor.fetchall()
        row = ''
        empid = ''
        for row in result:
            print(row)
            id_match = row['EmpID']
            search_hist_match = row['search_history']
            #source_ = row['SOURCE']
        print('emp id _match', type(id_match))
        #print('search_history_match_match', search_hist_match)
        #print('source', source)
        if (id_match == EmpID) and (search_hist_match == search_history):
            resp = jsonify(row)
            conn.commit()
            resp.status_code = 200
            return jsonify(message="EmpID, search_history already exist in table", error='false')
        elif (id_match != EmpID) and (search_hist_match != search_history):
            resp = jsonify(row)
            resp.status_code = 200
            sql = 'insert into usr_search_history(`EmpID`, `search_history`, `mark`) values(%s, %s, %s)'
            values = (EmpID, search_history, mark)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, values)
            conn.commit()
            print(cursor.rowcount, "record inserted.")
            return jsonify(message="search history added successfully in db", true='true')
    except Exception as e:
        print(e)
        print('exception raise in usr_search_history')
        return jsonify(message='exception raise in usr_search_history')
    finally:
        cursor.close()
        conn.close()


#for admin #####################################################################################################################################


@cross_origin()
@app.route('/admin_login', methods=['POST'])
def get_admin_login():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    PASSWORD = data['PASSWORD']
    print('EmpID ', EmpID)
    print('PASSWORD ', PASSWORD)
    name_match = ''
    password_match = ''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE EmpID = %s AND PASSWORD = %s'
    values = EmpID, PASSWORD
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        # print(row[7])
        name_match = row['EmpID']
        print('name matched ', name_match)
        password_match = row['PASSWORD']
        print('pass matched ', password_match)
        resp = jsonify(message="admin logged in successful ")
        return resp
    if EmpID == name_match:
        resp = jsonify(message="logged in successful ")
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(
            message="username or password did not match" + name_match,
            error='true'
        )
        resp.status_code = 405
        return resp

        '''if request.method == 'POST' and 'EmpID' in request.form and 'PASSWORD' in request.form:
            EmpID = request.form['EmpID']
            PASSWORD = request.form['PASSWORD']'''


@cross_origin(app, support_credential=True)
@app.route('/user_login', methods=['POST'])
def get_user_login():
    '''if request.method == 'POST' and 'EmpID' in request.values and 'PASSWORD' in request.values:
        EmpID = request.values['EmpID']
        PASSWORD = request.values['PASSWORD']
        print('EmpID ', EmpID)
        print('PASSWORD ',PASSWORD)'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    PASSWORD = data['PASSWORD']
    print('EmpID ', EmpID)
    print('EmpID type', type(EmpID))
    print('PASSWORD ', PASSWORD)
    name_match = ''
    password_match = ''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE EmpID = %s AND PASSWORD = %s'
    values = EmpID, PASSWORD
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        # print(row[7])
        name_match = row['EmpID']
        print('name matched ', name_match)
        password_match = row['PASSWORD']
        print('pass matched ', password_match)
        #resp = jsonify(message="user logged in successful ")
        # return resp
    if EmpID == name_match:
        resp = jsonify(message="logged in successful ", data=row)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(
            message="username or password did not match" + name_match,
            error='true'
        )
        resp.status_code = 405
        return resp

    '''if request.method == 'POST' and 'EmpID' in request.form and 'PASSWORD' in request.form:
        EmpID = request.form['EmpID']
        PASSWORD = request.form['PASSWORD']'''


@app.route('/get_user_data_by_id', methods=['POST'])
def get_user_data_by_id():
    data = request.get_json()
    print(data)
    id = data['id']
    # if request.method == 'POST' and 'EMAIL_ID' in request.form:
    # EmpID = request.form['EMAIL_ID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE Sr_No = %s'
    values = id
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        resp = jsonify(row)
        resp.status_code = 200
        return resp


@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    '''if request.method == 'POST' and 'EmpID' in request.form:
            EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE EmpID = %s'
    values = EmpID
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        resp = jsonify(row)
        resp.status_code = 200
        return resp


@app.route('/spell_correct', methods=['POST'])
def get_spell_correct():
    # spell_val=''
    '''if request.method == 'POST' and 'spell' in request.form:
        spell_val = request.form['spell']'''
    data = request.get_json()
    print(data)
    spell_val = data['spell']
    spell = Speller(lang='en')
    val = spell(spell_val)
    stringA = {"did_u_mean": val}
    print(stringA)
    print(spell(spell_val))
    resp = jsonify(stringA)
    resp.status_code = 200
    return resp



@cross_origin()
@app.route('/forget_password', methods=['POST'])
def get_forget_password():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        # EmpID = data['EmpID']
        EMAIL_ID = data['EMAIL_ID']
        # print('EmpID', EmpID)
        print('EMAIL_ID', EMAIL_ID)
        match = ''
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM registration WHERE EMAIL_ID=%s'
        values = (EMAIL_ID)
        cursor.execute(sql, values)
        result = cursor.fetchall()
        for row in result:
            print('row ', row['EMAIL_ID'])
            #cursor.execute("SELECT *FROM registration WHERE EMAIL_ID= '%s'" % EMAIL_ID+" AND EmpID='%s'"% EmpID)
            #cursor.execute("SELECT *FROM registration WHERE EMAIL_ID= '%s'" % EMAIL_ID)
            match = row['EMAIL_ID']
            #print('match 6 ', row[6])
        if EMAIL_ID == match:
            # Approach first
            # get random password pf length 8 with letters, digits, and symbols
            password_characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(password_characters)
                               for i in range(8))
            print("Random password is:", password)
            sql = "UPDATE registration SET PASSWORD=%s where EMAIL_ID=%s"
            val = (password, EMAIL_ID)
            cursor.execute(sql, val)
            conn.commit()
            print("password updated in db successfully ", password)

            # Output $z#m;-fb
            msg = MIMEText(password)
            msg['Subject'] = 'Use below password to login with ICAT'
            msg['From'] = 'icat@arde.org'
            msg['To'] = EMAIL_ID

            s = smtplib.SMTP('128.9.25.4:25')
            s.ehlo()
            #s.starttls()
            s.login('icat@arde.org', 'icat@123')
            s.sendmail('icat@arde.org', EMAIL_ID, msg.as_string())
            s.quit()
            return jsonify(message="email sent successfully on " + EMAIL_ID, true='true')
            # return resp
        else:
            return jsonify(message="id or email not matched u cannot reset the password", error='false')
            # return resp

    except Exception as e:
        print('forgot password api', e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update_user', methods=['PUT'])
def get_update_user():
    data = request.get_json()
    Name = data['name']
    Group_by = data['group']
    Designation = data['designation']
    PHONENO = data['phone']
    # value should send by front end devloper
    EMAIL_ID = data['email']
    EmpID = data['EmpID']
    print(Name)
    print(Group_by)
    print(Designation)
    print(PHONENO)
    print(EMAIL_ID)
    print(EmpID)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE registration SET Name=%s,Group_by=%s,Designation=%s,PHONENO=%s,EMAIL_ID=%s  WHERE EmpID=%s"
    values = (Name, Group_by, Designation, PHONENO, EMAIL_ID, EmpID)
    cursor.execute(sql, values)
    conn.commit()
    return jsonify(message='user updated successfuly')


@cross_origin()
@app.route('/registration', methods=['POST'])
def get_registration():
    try:
        data = request.get_json()
        print(data)
        EmpID = data['emp_id']
        EMAIL_ID = data['email']
        Name = data['name']
        Group_by = data['group']
        Designation = data['designation']
        PHONENO = data['phone']
        PASSWORD = data['password']
        print('EmpID',EmpID)
        print('EMAIL_ID',EMAIL_ID)
        print('Name',Name)
        print('Group_by',Group_by)
        print('Designation',Designation)
        print('PHONENO',PHONENO)
        id = ''
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('select *from registration')
        sql_idcheck = cursor.fetchall()
        for i in sql_idcheck:
            id = str(i['EmpID'])
            print('EmpID ',EmpID)
            print('id ',id)
            if EmpID == id:
                return jsonify(message="empid already exist try another empid!",true='true')
            elif EmpID != id:
                sql = 'insert into registration(`Sr_No`, `EmpID`, `Name`, `Group_by`, `Designation`, `PHONENO`, `EMAIL_ID`, `PASSWORD`) values(NULL, %s, %s,%s, %s,%s, %s, %s)'
                values = (EmpID, Name, Group_by, Designation,
                          PHONENO, EMAIL_ID, PASSWORD)
                cursor.execute(sql, values)
                conn.commit()
                print(cursor.rowcount, "record inserted.")
                return jsonify(message="registration succesfully",false='false')

    except Exception as e:
        print('registration api', e)
    finally:
        cursor.close()
        conn.close()


@app.route('/cpass', methods=['PUT'])
def get_cpass():
    '''if request.method == 'PUT' and 'EmpID' in request.form and 'PASSWORD' in request.form:
        EmpID = request.form['EmpID']
        PASSWORD = request.form['PASSWORD']'''
    data = request.get_json()
    PASSWORD = data['PASSWORD']
    EmpID = data['EmpID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE registration SET PASSWORD=%s WHERE EmpID=%s"
    values = (PASSWORD, EmpID)
    cursor.execute(sql, values)
    conn.commit()
    return jsonify(message='password changed successfully')


@ app.route('/get_data_by_empid', methods=['POST'])
def get_data_by_empid():
    '''if request.method == 'POST' and 'EmpID' in request.form:
        EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    # EmpID = request.form['EmpID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `registration` WHERE EmpID=%s" % (EmpID))
    result = cursor.fetchall()
    for row in result:
        print(row)
    resp = jsonify(row)
    resp.status_code = 200
    return resp


@app.route('/delete_by_empid', methods=['DELETE'])
def get_delete_by_empid():
    '''if request.method == 'DELETE' and 'EmpID' in request.form:
        EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    print('delete empid ', EmpID)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM `registration` WHERE EmpID=%s" % (EmpID))
    conn.commit()
    resp = jsonify(message='user deleted successfully')
    resp.status_code = 200
    return resp


@app.route('/delete_myfav_by_empid', methods=['POST'])
def get_delete_myfav_by_empid():
    '''if request.method == 'DELETE' and 'id' in request.form:
        id = request.form['id']'''
    data = request.get_json()
    print(data)
    id = data['id']
    print('delete id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM `usr_fav` WHERE id=%s" % (id))
    conn.commit()
    resp = jsonify(message='bookmark removed successfully')
    resp.status_code = 200
    return resp


@app.route('/delete_single_notification_by_id', methods=['DELETE'])
def get_delete_singlenoti_by_empid():
    '''if request.method == 'DELETE' and 'id' in request.form:
        id = request.form['id']'''
    data = request.get_json()
    print(data)
    id = data['id']
    print('delete id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM `usr_notification` WHERE id=%s" % (id))
    conn.commit()
    resp = jsonify(message='notification deleted successfully', true='true')
    resp.status_code = 200
    return resp


@app.route('/delete_all_notification_by_eid', methods=['DELETE'])
def get_delete_all_notification_by_eid():
    '''if request.method == 'DELETE' and 'EmpID' in request.form:
        EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    print('delete empid ', EmpID)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM `usr_notification` WHERE EmpID=%s" % (EmpID))
    conn.commit()
    resp = jsonify(
        message='all notification deleted by eid successfully', true='true')
    resp.status_code = 200
    return resp

@cross_origin()
@app.route('/notification_insert', methods=['POST'])
def get_notification_insert():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    FILEPATH = data['FILEPATH']
    SOURCE = data['SOURCE']
    DESCRIPTION = data['DESCRIPTION']
    MARK = "FALSE"


    print(EmpID)
    print(FILEPATH)
    print(SOURCE)
    print(DESCRIPTION)
    print(MARK)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = 'INSERT INTO `usr_notification`(`EmpID`, `FILEPATH`, `SOURCE`, `DESCRIPTION`, `mark`) VALUES (%s, %s, %s,%s,%s)'
    values = (EmpID, FILEPATH, SOURCE, DESCRIPTION, MARK)

    cursor.execute(sql, values)
    conn.commit()
    print(cursor.rowcount, "record inserted.")
    return jsonify(message="notified succesfully", true='true')


@app.route('/my_library_insert', methods=['GET', 'POST'])
def get_my_fav_insert():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    SOURCE = data['SOURCE']
    DESCRIPTION = data['DESCRIPTION']
    TITLE = data['TITLE']
    FILEPATH = data['FILEPATH']
    print(EmpID)
    print(SOURCE)
    print(DESCRIPTION)
    print(TITLE)
    print(FILEPATH)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print('EmpID ', EmpID)
    print('TITLE ', TITLE)
    email_match = ''
    TITLE_match = ''


    sql = "SELECT * FROM `usr_fav` WHERE EmpID=%s and TITLE=%s"
    values = (EmpID, TITLE)
    cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
    cursor.execute(sql, values)
    result = cursor.fetchall()
    row = ''
    for row in result:
        print(row)
        email_match = row['EmpID']
        TITLE_match = row['TITLE']
        print('email_match', email_match)
        print('TITLE_match', TITLE_match)
    if (email_match != EmpID) and (TITLE_match != TITLE):
        resp = jsonify(row)
        conn.commit()
        resp.status_code = 200
        # return jsonify(message="EmpID and title not exist in db", true='true')
        sql = 'INSERT INTO `usr_fav`(`EmpID`, `SOURCE`, `DESCRIPTION`, `TITLE`, `FILEPATH`) VALUES(%s, %s, %s, %s, %s)'
        values = (EmpID, SOURCE, DESCRIPTION, TITLE, FILEPATH)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="bookmarked succesfully", true='true')
    else:
        resp = jsonify(row)
        resp.status_code = 200
        return jsonify(message="EmpID and title exist in db", error='false')


@ cross_origin()
@ app.route('/get_library_record', methods=['POST'])
def get_library_record():
    data = request.get_json()
    print(data)
    mydictionary_res = {}
    mydictionary_res["res"] = []
    res = mydictionary_res["res"]
    EmpID = data['EmpID']
    print(EmpID)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM usr_fav WHERE EmpID = %s'
    values = EmpID
    cursor.execute(sql, values)
    result = cursor.fetchall()
    response = []
    for row in result:
        print(row)
        res.append(row)
        print(res)
        #resp = jsonify(row)
        #resp.status_code = 200
    combine_arr = {**mydictionary_res}
    resp = jsonify(combine_arr)
    return resp


'''@cross_origin()
@app.route('/usr_search_history', methods=['GET', 'POST'])
def get_usr_search_history():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    search_history = data['search_history']
    filepath = data['filepath']
    print('EmpID', EmpID)
    print('search history', search_history)
    print('filepath', filepath)

    print('EmpID ', EmpID)
    print('search_history ', search_history)
    email_match = ''
    search_history_match = ''
    # try:
    sql = "SELECT * FROM `usr_search_history` WHERE EmpID=%s and search_history=%s"
    values = (EmpID, search_history_match)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    row = ''
    for row in result:
        print(row)
        email_match = row['EmpID']
        search_history_match = row['search_history']
        print('email_match', email_match)
        print('search_history_match_match', search_history_match)
    if (email_match == EmpID) and (search_history_match == search_history):
        resp = jsonify(row)
        conn.commit()
        resp.status_code = 200
        return jsonify(message="EmpID and search_history exist in db", error='false')

    elif (email_match != EmpID) and (search_history_match != search_history):
        resp = jsonify(row)
        resp.status_code = 200
        # return jsonify(message="EmpID and title not exist in db", true='true')
        sql = 'insert into usr_search_history(`EmpID`, `search_history`,`filepath`) values(%s, %s, %s)'
        values = (EmpID, search_history, filepath)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="search history added successfully in db", true='true')'''


# get all my fav list by empid
@app.route('/all_mylibrary_list', methods=['POST'])
def get_all_mylibrary_list():
    '''if request.method == 'POST' and 'EmpID' in request.form:
        EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    print(EmpID)

    mydictionary_res = {}
    mydictionary_res["res"] = []
    res = mydictionary_res["res"]

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT DISTINCT TITLE from usr_fav WHERE EmpID= %s'
    values = EmpID
    cursor.execute(sql, values)
    result = cursor.fetchall()
    response = []
    for row in result:
        print(row)
        res.append(row)
        print(res)
        # resp = jsonify(row)
        # resp.status_code = 200
    combine_arr = {**mydictionary_res}
    resp = jsonify(combine_arr)
    return resp
# 3333333333333


@app.route('/notification_count', methods=['POST'])
def get_notification_count():
    data = request.get_json()
    EmpID = data['EmpID']
    print('notification_count empid ', EmpID)
    MARK = "FALSE"
    print('false ', MARK)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        #sql_val = 'SELECT COUNT(*) FROM usr_notification WHERE mark=%s AND EmpID=%s'
       # sql_val = 'SELECT count( DISTINCT(search_hst) ) FROM usr_notification WHERE mark=%s AND EmpID=%s'
        sql_val = 'SELECT count(search_hst) FROM usr_notification WHERE mark=%s AND EmpID=%s'
        values = (MARK, EmpID)
        cursor.execute(sql_val, values)
        result = cursor.fetchall()
        print('count result ',result)
        #
        for row in result:
            row['COUNT'] = row.pop('count(search_hst)')
            print('row child', row)
            resp = row
            return resp
    except Exception as e:
        print(e)
        print('notification count api got exception')
        return jsonify(message='notification count api got exception')
    finally:
        cursor.close()
        conn.close()



@app.route("/notification_hide", methods=['POST'])
def getnotification_hide():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    MARK = 'TRUE'
    print('notification_hide empid ', EmpID)
    #print('notification_hide mark ', MARK)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "UPDATE usr_notification SET mark=%s WHERE EmpID=%s"
        values = (MARK, EmpID)
        cursor.execute(sql, values)
        conn.commit()
        sql_val = "select mark,EmpID from usr_notification where mark=%s AND EmpID=%s"
        values = (MARK, EmpID)
        cursor.execute(sql_val, values)
        result = cursor.fetchall()
        mark_value = ''
        EmpID_value = ''
        for i in result:
            EmpID_value = str(i['EmpID'])
            mark_value = str(i['mark'])
        #print('mark_value ',type(mark_value))
        #print('EmpID_value ',type(EmpID_value))
        if (EmpID == EmpID_value) and (MARK == mark_value):
            resp = jsonify(EmpID)
            conn.commit()
            resp.status_code = 200
            return jsonify(message='notification count is hidden successfully ', true='true')
        elif (EmpID != EmpID_value):
            resp = jsonify(EmpID)
            resp.status_code = 200
            return jsonify(message='empid is not exit is notification table ', false='false')
        else:
            resp = jsonify(EmpID)
            resp.status_code = 200
            return jsonify(message="other exception in db", error='false')
    except Exception as e:
        print(e)
        print('notification hide api got exception')
        return jsonify(message='notification hide api got exception')
    finally:
        cursor.close()
        conn.close()


@app.route('/all_notification', methods=['POST'])
def get_all_notification():
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    print(EmpID)

    mydictionary_res = {}
    mydictionary_res["res"] = []
    res = mydictionary_res["res"]

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    #sql = 'SELECT * FROM usr_notification WHERE EmpID = %s' #return same value with multiple times
    sql = 'SELECT * FROM usr_notification WHERE EmpID=%s'
    values = EmpID
    cursor.execute(sql, values)
    result = cursor.fetchall()
    response = []
    for row in result:
        print(row)
        res.append(row)
        print(res)
        # resp = jsonify(row)
        # resp.status_code = 200
    combine_arr = {**mydictionary_res}
    resp = jsonify(combine_arr)
    return resp


@app.route('/admin_all_user', methods=['GET'])
def admin_all_user():
    conn = None
    cursor = None
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from registration")
            row = cursor.fetchall()
            # users.append(row)
            # combine_arr = {**mydictionary_users}
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('admin_all_user not found', 500)
            return resp
        else:
            resp = jsonify('no country found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print('admin_all_user', e)
    finally:
        cursor.close()
        conn.close()


@app.route('/coordinators', methods=['GET'])
def get_coordinators():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["coordinators"] = []
        res = mydictionary_res["coordinators"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = coordinators_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ',tup)
            #print('coordinators_db global',coordinators_db)
            result = tuple(set(tup))
            #str2=''.join(result)
            #status_list=str2.split()
            #print('coordinators_db list ',result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"coordinators": temp})
                print('res',res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no institute found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        #for clear institute data
        coordinators_db.clear()
        cursor.close()
        conn.close()


#JANES FILETER LIST######################################################################################################################################


@app.route('/status', methods=['GET'])
def get_status():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["status"] = []
        res = mydictionary_res["status"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = status_db
            tup = tuple(lst)
            #print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('status_db global', status_db)
            result = tuple(set(tup))
            str2 = ','.join(result)
            status_list = str2.split()
            #print('status_list ', status_list)
            for temp in status_list:
                for split_result in temp.split(','):
                    res.append({"status": split_result})
                    #print(res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no status found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear status data
        status_db.clear()
        cursor.close()
        conn.close()


@app.route('/country', methods=['GET'])
def get_country():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["country"] = []
        res = mydictionary_res["country"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = country_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('country_db global', country_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('status country_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"country": temp})
                #print('res in country ', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no status found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear country data
        country_db.clear()
        cursor.close()
        conn.close()


@app.route('/section', methods=['GET'])
def get_section():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["section"] = []
        res = mydictionary_res["section"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = section_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('section_db global', section_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('section_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"section": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no status found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear section data
        section_db.clear()
        cursor.close()
        conn.close()


@ app.route('/general_title', methods=['GET'])
def get_general_title():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["gt"] = []
        res = mydictionary_res["gt"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = general_title_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('general_title_db global', general_title_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('general_title list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"gn": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no status found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear general_title data
        general_title_db.clear()
        cursor.close()
        conn.close()

#JANES WISE FILTER #########################################################################################################################################


@ app.route("/country_wise", methods=['POST'])
def country_wise():
    '''if request.method == 'POST' and 'country_var' in request.values:
        country_var = request.values['country_var']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        country_var = request.json['country_var']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(country_var, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `hand` WHERE country=\"" + country_var + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List country is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/section_wise", methods=['POST'])
def section_wise():
    '''if request.method == 'POST' and 'section_var' in request.values:
        section_var = request.values['section_var']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        section_var = request.json['section_var']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(section_var, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `hand` WHERE section=\""+section_var+"\"")
        row = cursor.fetchall()
        if not row:
            print("List section is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/company_wise", methods=['GET', 'POST'])
def section_company():
    '''if request.method == 'POST' and 'company' in request.values:
        company = request.values['company']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        company = request.json['company']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(company, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `hand` WHERE company=\"" + company + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List company_wise is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('company_wise  result not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/general_title_wise", methods=['POST'])
def general_title_wise():
    '''if request.method == 'POST' and 'general_title' in request.values:
        general_title = request.values['general_title']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        general_title = request.json['general_title']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(general_title, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `hand` WHERE general_title=\"" + general_title + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List general_title is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('general_title result not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/company", methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        company = request.json['company']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(company, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `hand` WHERE company=\""+company+"\"")
            # "select * from child_real where coordinators=%s;"%user)
            # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
            row = cursor.fetchall()
            if not row:
                print("List general_title is empty")
            resp = jsonify(row)
            resp.status_code = 200
            return jsonify(message="successfully fetched status data!")

        except Exception as e:
            print(e)
            print('general_title result not found')
        finally:
            cursor.close()
            conn.close()

#NPTEL FILETER LIST ####################################################################################################################################


@app.route('/subjectName', methods=['GET'])
def get_subjectName():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["subjectName"] = []
        res = mydictionary_res["subjectName"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = subjectName_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('subjectName_db global', subjectName_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('subjectName_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"subjectName": temp})
                print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in subjectName', 500)
            return resp
        else:
            resp = jsonify('no subjectName found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear subjectName data
        subjectName_db.clear()
        cursor.close()
        conn.close()




@app.route('/institute', methods=['GET'])
def get_institute():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["institute"] = []
        res = mydictionary_res["institute"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = institute_db
            tup = tuple(lst)
            print(type(tup))
            #('list converted to tuple = ', tup)
            #print('institute_db global', institute_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('institute_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"institute": temp})
                print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no institute found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear institute data
        institute_db.clear()
        cursor.close()
        conn.close()


@app.route('/filetype', methods=['GET'])
def get_filetype():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["institute"] = []
        res = mydictionary_res["institute"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = filetype_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('filetype_db global', filetype_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('filetype_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"filetype": temp})
                print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in status', 500)
            return resp
        else:
            resp = jsonify('no filetype found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear filetype data
        filetype_db.clear()
        cursor.close()
        conn.close()


@app.route('/disciplineName', methods=['GET'])
def get_disciplineName():
    conn = None
    cursor = None
    try:
        mydictionary_res = {}
        mydictionary_res["disciplineName"] = []
        res = mydictionary_res["disciplineName"]
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            lst = disciplineName_db
            tup = tuple(lst)
            print(type(tup))
            #print('list converted to tuple = ', tup)
            #print('disciplineName_db global', disciplineName_db)
            result = tuple(set(tup))
            # str2=''.join(result)
            # status_list=str2.split()
            #print('disciplineName_db list ', result)
            for temp in result:
                '''for split_result in temp.split(' '):'''
                res.append({"disciplineName": temp})
                #print('res', res)
            resp = jsonify(res)
            return resp
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('data not found in disciplineName', 500)
            return resp
        else:
            resp = jsonify('no disciplineName found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        # for clear disciplineName data
        disciplineName_db.clear()
        cursor.close()
        conn.close()

#NPTEL FILTER WISE LIST #########################################################################################################################################


@app.route("/coordinators_id", methods=['POST'])
def coordinators_id():
    '''if request.method == 'POST' and 'coordinator' in request.values:
        coordinator = request.values['coordinator']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        coordinator = request.json['coordinator']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(coordinator, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `child_real` WHERE coordinators=\"" + coordinator + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List filetype_id is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('filetype not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/subjectName_id", methods=['GET', 'POST'])
def subjectName_id():
    '''if request.method == 'POST' and 'subjectName' in request.values:
        subjectName = request.values['subjectName']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        subjectName = request.json['subjectName']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(subjectName, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `child_real` WHERE subjectName=\"" + subjectName + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List subjectName_id is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@app.route("/disciplineName_id", methods=['GET', 'POST'])
def disciplineName_id():
    '''if request.method == 'POST' and 'disciplineName' in request.values:
        disciplineName = request.values['disciplineName']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        disciplineName = request.json['disciplineName']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(disciplineName, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `child_real` WHERE disciplineName=\"" + disciplineName + "\"")
        row = cursor.fetchall()
        if not row:
            print("List  filetype_id is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@ app.route("/filetype_id", methods=['POST'])
def filetype_id():
    '''if request.method == 'POST' and 'filetype' in request.values:
        filetype = request.values['filetype']'''
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        filetype = request.json['filetype']
        # coordinator = 'Dr. Liza Das'
        parser.add_argument(filetype, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `child_real` WHERE filetype=\"" + filetype + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List filetype_id is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@app.route("/institute_id", methods=['POST'])
def institute_id():
    if request.method == 'POST' and 'institute' in request.values:
        institute = request.values['institute']
    '''if request.method == 'POST':
        parser = reqparse.RequestParser()
        institute = request.json['institute']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(institute, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)'''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # inserting the values into the table
        cursor.execute(
            "SELECT * FROM `child_real` WHERE institute=\"" + institute + "\"")
        # "select * from child_real where coordinators=%s;"%user)
        # "select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
        row = cursor.fetchall()
        if not row:
            print("List institute_id is empty")
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@app.route("/EmpID_exist", methods=['POST'])
def empid_exist():
    '''if request.method == 'POST' and 'EmpID' in request.form:
        EmpID = request.form['EmpID']'''
    data = request.get_json()
    print(data)
    EmpID = data['EmpID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print('EmpID ', EmpID)
    email_match = ''
    try:
        sql = "SELECT * FROM `registration` WHERE EmpID=%s"
        values = EmpID
        cursor.execute(sql, values)
        row = cursor.fetchone()
        print(row)
        email_match = row['EmpID']
        print(email_match)
        if email_match == EmpID:
            resp = jsonify(row)
            conn.commit()
            resp.status_code = 200
            return jsonify(message="EmpID not exist in db", true='true')
        else:
            resp = jsonify(row)
            resp.status_code = 500
            return jsonify(message="EmpID exist in db", error='false')
    except Exception as e:
        print(e)
        print('empid_exist result not found')
        return jsonify(message='EmpID does not exist in db')
    finally:
        cursor.close()
        conn.close()


@app.route('/admin_all_user', methods=['GET'])
def admin_all_user2():
    conn = None
    cursor = None
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from registration")
            row = cursor.fetchall()
            # users.append(row)
            # combine_arr = {**mydictionary_users}
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success', 200)
            elif resp == 500:
                print('admin_all_user not found', 500)
            return resp
        else:
            resp = jsonify('no country found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print('admin_all_user', e)
    finally:
        cursor.close()
        conn.close()


@app.route('/admin_search', methods=['GET'])
def get_admin_search():
    conn = None
    cursor = None
    try:
        jsearch = request.args.get('q')
        print('user entered : -', jsearch)
        if jsearch:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from registration where EmpID LIKE\"%" + jsearch + "%\" OR Name LIKE \"%" + jsearch + "%\" OR Group_by LIKE \"%" +
                           jsearch + "%\" OR Designation LIKE\"%" + jsearch + "%\" OR PHONENO LIKE \"%" + jsearch + "%\" OR EMAIL_ID like \"%" + jsearch + "%\"")
            row = cursor.fetchall()
            if not row:
                print("List is empty")
            resp = jsonify(row)
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
        print('result not found')
    finally:
        cursor.close()
        conn.close()


@app.route('/update_user_by_admin', methods=['PUT'])
def get_update_user_by_admin():
    data = request.get_json()
    Name = data['name']
    Group_by = data['group']
    Designation = data['designation']
    PHONENO = data['phone']
    # value should send by front end devloper
    EMAIL_ID = data['email']
    empID = data['emp_id']
    PASSWORD = data['PASSWORD']
    ROLE = data['role']
    Sr_No = data['id']
    print(Name)
    print(Group_by)
    print(Designation)
    print(PHONENO)
    print(EMAIL_ID)
    print(PASSWORD)
    print(Sr_No)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE registration SET Name=%s,Group_by=%s,Designation=%s,PHONENO=%s,PASSWORD=%s,EmpID=%s,ROLE=%s WHERE Sr_No=%s"
    values = (Name, Group_by, Designation, PHONENO,
              PASSWORD, empID, ROLE, Sr_No)
    cursor.execute(sql, values)
    conn.commit()
    return jsonify(message='user updated by admin successfuly')

@ app.route('/get_data_by_emailid', methods=['POST'])
def get_data_by_emailid():
    if request.method == 'POST' and 'EmpID' in request.values:
        EmpID = request.values['EmpID']
        '''data = request.get_json()
        print(data)
        EmpID = data['EmpID']'''
        #EMAIL_ID = request.values['EMAIL_ID']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM `registration` WHERE EmpID=%s"
        values = EmpID
        cursor.execute(sql, values)
        result = cursor.fetchall()
        for row in result:
            print(row)
            resp = jsonify(row)
            resp.status_code = 200
            return resp


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='128.9.32.52')
    CORS(app)

