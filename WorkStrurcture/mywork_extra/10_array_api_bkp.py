import pymysql
from app import app
from db import mysql
from mock import Mock, patch
import json
import difflib
from flask import jsonify, request
import collections
from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api, reqparse
import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_cors import CORS, cross_origin
import psycopg2

'''
try:
    dconn = psycopg2.connect(database="dspace",
                             user="postgres",
                             password="postgres",
                             host="127.0.0.1",
                             port="5432")
    print("postgres database connected")
except:
    print("please check your dspace server is on")
'''

@app.route('/common_db', methods=['GET', 'POST'])
def get_user():
    conn = None;
    cursor = None;
    try:
        mydictionary_nptel = {}
        mydictionary_nptel["nptel"] = []
        nptel = mydictionary_nptel["nptel"]

        mydictionary_janes = {}
        mydictionary_janes["janes"] = []
        janes = mydictionary_janes["janes"]

        mydictionary_libsys = {}
        mydictionary_libsys["libsys"] = []
        libsys = mydictionary_libsys["libsys"]

        mydictionary_arma = {}
        mydictionary_arma["arma"] = []
        arma = mydictionary_arma["arma"]

        mydictionary_dspace = {}
        mydictionary_dspace["dspace"] = []
        dspace = mydictionary_dspace["dspace"]
        # creation of empty arraylist
        #csearch = request.args.get('q')
        csearch = 'india'
        if csearch:
            #dspace_cur = dconn.cursor()
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "select * from child_real where coordinators LIKE\"%" + csearch + "%\" OR disciplineName LIKE \"%" + csearch + "%\" OR subjectName LIKE \"%" + csearch + "%\" OR institute LIKE\"%" + csearch + "%\" OR filetype LIKE \"%" + csearch + "%\" OR lect_name like \"%" + csearch + "%\"")
            child_real_rows = cursor.fetchall()
            for row in child_real_rows:
                nptel.append(row)

            cursor.execute("select * from hand where country LIKE\"%" + csearch + "%\"")
            hand_janes = cursor.fetchall()
            for jrow in hand_janes:
                janes.append(jrow)

            cursor.execute("select * from lib where BUDGT_HEAD_NAME LIKE\"%" + csearch + "%\"")
            lib = cursor.fetchall()
            for jrow in lib:
                libsys.append(jrow)

            cursor.execute("select * from wp_comments where comment_author LIKE\"%" + csearch + "%\"")
            wp_comments_janes = cursor.fetchall()
            for jrow in wp_comments_janes:
                arma.append(jrow)

            cursor.execute("SELECT * FROM dspace WHERE text_value LIKE\"%"+ csearch + "%\"")
            metadatavalue_janes = cursor.fetchall()
            for jrow in metadatavalue_janes:
                dspace.append(jrow)

            combine_arr = {**mydictionary_nptel, **mydictionary_janes,**mydictionary_arma,**mydictionary_dspace,
                           **mydictionary_libsys}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

    except Exception as e:
        print(e)
        print('exception found')
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
