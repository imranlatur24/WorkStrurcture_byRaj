import smtplib
from email.mime.text import MIMEText
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import json
from flask_cors import CORS

from app import app
from flask_cors import CORS, cross_origin


try:
    testing_conn = mysql.connector.connect(host="localhost",user="root",password="root123",db="novetrics")
    print("drdo registration database connected")
except ConnectionRefusedError:
    print("please check your drdo database server is on")
except:
    print("connection problem in drdo database")

@cross_origin()
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'name' in request.values and 'password' in request.values:
        name = request.values['name']
        password = request.values['password']
        testing_cur = testing_conn.cursor()
        sql ='SELECT * FROM register WHERE name = %s AND password = %s'
        values = name,password
        testing_cur.execute(sql,values)
        account = testing_cur.fetchone()
        print(account)
    return jsonify(message="logged in without session")

'''
@cross_origin()
@app.route('/forget_password',methods=['POST'])
def get_forget_password():
    conn = None;
    cursor = None;
    sr_no = request.form.get("sr_no")
    email = request.form.get("email")
    print(request.get_json())
    print('email',email)
    data = request.get_json()
    sr_no = data['sr_no']
    email = data['email']
    print('email', email)
    match=''
    testing_cur = testing_conn.cursor()
    testing_cur.execute("SELECT *FROM register WHERE email= '%s'" % email+" AND sr_no='%s'"% sr_no)
    result = testing_cur.fetchall()
    for row in result:
      print(row[3])
      match = row[3]
    if email == match:
        msg = MIMEText('https://youtu.be/-Ecn2pbTcFU?list=RD-Ecn2pbTcFU')
        msg['Subject'] = 'CLICK HERE TO RESET YOUR PASSWORD'
        msg['From'] = 'imran.novetrics@gmail.com'
        msg['To'] = email

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login('imran.novetrics@gmail.com', 'Imran@dell@786ok')
        s.sendmail('novetrics.test@gmail.com', email, msg.as_string())
        s.quit()
        return jsonify(message="email sent successfully on "+email)
        return resp
    else:
        return jsonify(message="id or email not matched u cannot reset the password")
        return resp
'''
@cross_origin()
@app.route('/cpass', methods =['GET', 'PUT'])
def cpass():
    if request.method == 'PUT' and 'password' in request.values and 'sr_no' in request.values:
        password = request.values['password']
        sr_no = request.values['sr_no']
        testing_cur = testing_conn.cursor()
        testing_cur.execute("UPDATE register SET password=%s WHERE sr_no=%s" % (password,sr_no))
        testing_conn.commit()
        return jsonify(message="password changed successfully")

@cross_origin()
@app.route('/my_fav', methods =['GET', 'POST'])
def my_fav():
    if request.method == 'POST' and 'user_id' in request.values and 'my_fav' in request.values:
        user_id = request.values['user_id']
        my_fav = request.values['my_fav']
        sql = 'insert into usr_fav(`id`, `user_id`, `my_fav`) values(NULL, %s, %s)'
        values = (user_id,my_fav)
        testing_cur = testing_conn.cursor()
        testing_cur.execute(sql, values)
        testing_conn.commit()
        print(testing_cur.rowcount, "record inserted.")
    return jsonify(message="bookmarked succesfully")

@cross_origin()
@app.route('/notification', methods =['GET', 'POST'])
def search_hst():
    if request.method == 'POST' and 'user_id' in request.values and 'search_hst' in request.values:
        user_id = request.values['user_id']
        search_hst = request.values['search_hst']
        sql = 'insert into usr_notification(`id`, `user_id`, `search_hst`) values(NULL, %s, %s)'
        values = (user_id,search_hst)
        testing_cur = testing_conn.cursor()
        testing_cur.execute(sql, values)
        testing_conn.commit()
        print(testing_cur.rowcount, "record inserted.")
    return jsonify(message="notified succesfully")

if __name__ == "__main__":
   app.run(debug=True)
   CORS(app)


