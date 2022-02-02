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
from datetime import datetime

app = Flask(__name__)
CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testing'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@cross_origin(app, support_credential=True)
@app.route('/user_login', methods=['GET','POST'])
def get_user_login():
    #working for android side
    if request.method == 'POST' and 'empid' in request.values and 'password' in request.values:
        EmpID = request.values['empid']
        PASSWORD = request.values['password']
        print('EmpID ', EmpID)
        print('PASSWORD ',PASSWORD)
    name_match = ''
    password_match = ''
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM test WHERE empid = %s AND password = %s'
    values = EmpID, PASSWORD
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print('json',row)
        # print(row[7])
        name_match = row['empid']
        print('name matched ', name_match)
        password_match = row['password']
        print('pass matched ', password_match)
        #resp = jsonify(message="user logged in successful ")
        # return resp
    if EmpID == name_match:
        resp = jsonify(resp=200,User=row)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(
            message="username or password did not match" + name_match,
            error='true'
        )
        resp.status_code = 405
        return resp

@cross_origin(app, support_credential=True)
@app.route('/user_register', methods=['POST'])
def get_user_register():
    try:
        #working for android side
        if request.method == 'POST' and 'first_name' in request.values and 'last_name' in request.values and 'empid' in request.values and 'sci_type' in request.values and 'password' in request.values and 'cpassword' in request.values and 'birth_date' in request.values:
            first_name = request.values['first_name']
            last_name = request.values['last_name']
            EmpID = request.values['empid']
            sci_type = request.values['sci_type']
            PASSWORD = request.values['password']
            CPASSWORD = request.values['cpassword']
            birth_date = request.values['birth_date']
            print('first_name ', first_name)
            print('last_name ', last_name)
            print('EmpID ', EmpID)
            print('sci_type ', sci_type)
            print('PASSWORD ', PASSWORD)
            print('CPASSWORD ', CPASSWORD)
            print('birth_date ', birth_date)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO `test`(`id`, `first_name`, `last_name`, `empid`, `sci_type`, `password`, `cpassword`, `birth_date`) values(NULL, %s, %s,%s, %s,%s, %s, %s)'
        values = (first_name, last_name, EmpID, sci_type, PASSWORD, CPASSWORD,birth_date)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="registration succesfully", false='false')
    except Exception as e:
        print('registration api', e)
    finally:
        cursor.close()
        conn.close()

@app.route('/callChangePassword', methods=['PUT'])
def get_cpass():
    try:
        if request.method == 'PUT' and 'id' in request.form and 'password' in request.form and 'cpassword' in request.form:
            id = request.form['id']
            PASSWORD = request.form['password']
            cPASSWORD = request.form['cpassword']
        # data = request.get_json()
        # PASSWORD = data['PASSWORD']
        # EmpID = data['EmpID']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "UPDATE test SET password=%s and cpassword=%s WHERE id=%s"
        values = (PASSWORD,cPASSWORD, 2)
        cursor.execute(sql, values)
        conn.commit()
        return jsonify(message='password changed successfully')
    except Exception as e:
        print('change password api', e)
    finally:
        cursor.close()
        conn.close()


id=0
@cross_origin(app, support_credential=True)
@app.route('/birth_alert', methods=['GET'])
def get_birth_alert():
    try:
        current_date = datetime.today().strftime('%d/%m/%Y')
        print('current date ',current_date)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM `test` WHERE birth_date=%s"
        values=current_date
        cursor.execute(sql,values)
        result = cursor.fetchall()
        for i in result:
            get_date =i['birth_date']
            id = i['id']
            print('get date ',get_date)
            if current_date == get_date:
                # resp = jsonify(EmpID)
                # resp.status_code = 200

                return jsonify(message='notification sent to  ')
            else:
                return jsonify(message='no birthday available')

            return ''
    except Exception as e:
        print('birth_alert api', e)
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='192.168.0.105')
    CORS(app)
