import smtplib
from email.mime.text import MIMEText
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import json
from flask_cors import CORS
import pymysql
from flask_restful import reqparse
from flask_cors import CORS, cross_origin
from config.app import app
from flaskext.mysql import MySQL
from register_drdo_db import mysql

#common db ########################################################################################################################################

csearch=''
'''@app.route('/common_db', methods=['GET'])
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

            combine_arr = {**mydictionary_nptel, **mydictionary_janes,**mydictionary_arma,
                           **mydictionary_libsys}
            resp = jsonify(combine_arr)
            resp.status_code = 200
            return resp

    except Exception as e:
        print(e)
        print('exception found')
    finally:
        cursor.close()
        conn.close()'''
#for admin #####################################################################################################################################
@cross_origin()
@app.route('/admin_login', methods=['POST'])
def get_admin_login():
    data = request.get_json()
    print(data)
    name = data['Name']
    password = data['PASSWORD']
    print('Name ', name)
    print('PASSWORD ', password)
    name_match = ''
    password_match = ''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE Name = %s AND PASSWORD = %s'
    values = name, password
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        #print(row[7])
        name_match = row['Name']
        print('name matched ', name_match)
        password_match = row['PASSWORD']
        print('pass matched ', password_match)
        resp = jsonify(message="admin logged in successful ")
        return  resp
    if name == name_match:
        resp = jsonify(message="logged in successful ")
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(     message="username or password did not match" + name_match)
        resp.status_code = 405
        return resp

@cross_origin()
@app.route('/user_login', methods=['POST'])
def get_user_login():
    data = request.get_json()
    print(data)
    name = data['Name']
    password = data['PASSWORD']
    print('Name ', name)
    print('PASSWORD ', password)
    email_match = ''
    password_match = ''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM registration WHERE EMAIL_ID = %s AND PASSWORD = %s'
    values = name, password
    cursor.execute(sql, values)
    result = cursor.fetchall()
    for row in result:
        print(row)
        #print(row[7])
        name_match = row['EMAIL_ID']
        print('name matched ', name_match)
        password_match = row['PASSWORD']
        print('pass matched ', password_match)
        resp = jsonify(message="email logged in successful ")
        return  resp
    if name == email_match:
        resp = jsonify(message="logged in successful ",error="false")
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(message="email or password did not match" + email_match,
                            error="true")
        resp.status_code = 405
        return resp

@cross_origin()
@app.route('/forget_password',methods=['POST'])
def get_forget_password():
    conn = None;
    cursor = None;
    try:
        #FOR POSTMAN TESTING
        #EmpID = request.form.get("EmpID")
        #EMAIL_ID = request.form.get("EMAIL_ID")
        #print(request.get_json())
        #print('EMAIL_ID',EMAIL_ID)

        #FOR JAVASCRIPT TESTING
        data = request.get_json()
        EmpID = data['EmpID']
        EMAIL_ID = data['EMAIL_ID']
        print('EmpID', EmpID)
        print('EMAIL_ID', EMAIL_ID)
        match=''
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM registration WHERE EMAIL_ID=%s AND EmpID=%s'
        values = (EmpID,EMAIL_ID)
        cursor.execute(sql, values)
        result = cursor.fetchall()
        for row in result:
            print(row)
        #cursor.execute("SELECT *FROM registration WHERE EMAIL_ID= '%s'" % EMAIL_ID+" AND EmpID='%s'"% EmpID)
            match = row[6]
        if EMAIL_ID == match:
            msg = MIMEText('https://youtu.be/-Ecn2pbTcFU?list=RD-Ecn2pbTcFU')
            msg['Subject'] = 'CLICK HERE TO RESET YOUR PASSWORD'
            msg['From'] = 'imran.novetrics@gmail.com'
            msg['To'] = EMAIL_ID

            s = smtplib.SMTP('smtp.gmail.com:587')
            s.starttls()
            s.login('imran.novetrics@gmail.com', 'Imran@dell@786ok')
            s.sendmail('novetrics.test@gmail.com', EMAIL_ID, msg.as_string())
            s.quit()
            return jsonify(message="email sent successfully on "+EMAIL_ID)
            return resp
        else:
            return jsonify(message="id or email not matched u cannot reset the password")
            return resp
    except Exception as e:
        print('forgot password api',e)
    finally:
        cursor.close()
        conn.close()

@app.route('/admin_search',methods=['GET'])
def get_admin_search():
    conn = None;
    cursor = None;
    try:
        jsearch = request.args.get('q')
        print('user entered : -', jsearch)
        if jsearch:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from registration where EmpID LIKE\"%" + jsearch + "%\" OR Name LIKE \"%" + jsearch + "%\" OR Group_by LIKE \"%" + jsearch + "%\" OR Designation LIKE\"%" + jsearch + "%\" OR PHONENO LIKE \"%" + jsearch + "%\" OR EMAIL_ID like \"%" + jsearch + "%\"")
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

@app.route('/cpass', methods=['PUT'])
def get_cpass():
    data = request.get_json()
    PASSWORD = data['PASSWORD']
    EMAIL_ID = data['EMAIL_ID']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE registration SET PASSWORD=%s WHERE EMAIL_ID=%s"
    values = (PASSWORD, EMAIL_ID)
    cursor.execute(sql, values)
    conn.commit()
    return jsonify(message='password changed successfuly')

@cross_origin()
@app.route('/registration', methods=['POST'])
def get_registration():
    try:
        # if request.method == 'POST' and 'EmpID' in request.values and 'Name' in request.values and 'Group_by' in request.values and 'Designation' in request.values and 'PHONENO' in request.values and 'EMAIL_ID' in request.values:
        '''EmpID = request.values['EmpID']
        Name = request.values['Name']
        Group_by = request.values['Group_by']
        Designation = request.values['Designation']
        PHONENO = request.values['PHONENO']
        EMAIL_ID = request.values['EMAIL_ID']

        testing_cur = testing_conn.cursor()
        testing_cur.execute("select *from registration where EmpID=%"%EmpID)
        result = testing_cur.fetchone()
        print(result)'''
        data = request.get_json()
        print(data)
        EmpID = 1010
        EMAIL_ID = data['email']
        Name = data['name']
        Group_by = data['group']
        Designation = data['designation']
        PHONENO = data['phone']
        PASSWORD = data['password']

        sql = 'insert into registration(`Sr_No`, `EmpID`, `Name`, `Group_by`, `Designation`, `PHONENO`, `EMAIL_ID`, `PASSWORD`) values(NULL, %s, %s,%s, %s,%s, %s, %s)'
        values = (EmpID, Name, Group_by, Designation,
                  PHONENO, EMAIL_ID, PASSWORD)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="registration succesfully")
    except Exception as e:
        print('registration api', e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update_user', methods=['PUT'])
def get_update_user():
    '''if request.method == 'PUT' and 'Name' in request.form and 'Group_by' in request.form and 'Designation' in request.form and 'PHONENO' in request.form and 'EMAIL_ID':
        Name = request.form['Name']
        Group_by = request.form['Group_by']
        Designation = request.form['Designation']
        PHONENO = request.form['PHONENO']
        EMAIL_ID = request.form['EMAIL_ID']'''
    data = request.get_json()
    Name = data['Name']
    Group_by = data['Group_by']
    Designation = data['Designation']
    PHONENO = data['PHONENO']
    #value should send by front end devloper
    EMAIL_ID = request.form['EMAIL_ID']
    print(Name)
    print(Group_by)
    print(Designation)
    print(PHONENO)
    print(EMAIL_ID)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE registration SET Name=%s,Group_by=%s,Designation=%s,PHONENO=%s WHERE EMAIL_ID=%s"
    values = (Name,Group_by,Designation,PHONENO,EMAIL_ID)
    cursor.execute(sql,values)
    conn.commit()
    return jsonify(message='user updated successfuly')


@app.route('/deleteall_noti_user_id', methods=['DELETE'])
def get_deleteall_noti_user_id():
        '''if request.method == 'DELETE' and 'user_id' in request.form:
            user_id = request.form['user_id']'''
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        print('delete noti user_id ',user_id)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM `usr_notification` WHERE user_id=%s" % (user_id))
        conn.commit()
        resp = jsonify(message='notification deleted successfully')
        resp.status_code = 200
        return resp

@app.route('/delete_noti_user', methods=['DELETE'])
def get_delete_noti_empid():
    '''if request.method == 'DELETE' and 'id' in request.form:
        id = request.form['id']'''
    data = request.get_json()
    print(data)
    id = data['id']
    print('delete noti id ', id)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM `usr_notification` WHERE id=%s" % (id))
    conn.commit()
    resp = jsonify(message='notification deleted successfully')
    resp.status_code = 200
    return resp


@app.route('/get_data_by_empid', methods=['POST'])
def get_data_by_empid():
        #if request.method == 'POST' and 'EmpID' in request.form:
            data = request.get_json()
            print(data)
            EmpID = data['EmpID']
            #EmpID = request.form['EmpID']
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
        #if request.method == 'DELETE' and 'EmpID' in request.form:
        #    EmpID = request.form['EmpID']
            data = request.get_json()
            print(data)
            EmpID = data['EmpID']
            print('delete empid ',EmpID)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("DELETE FROM `registration` WHERE EmpID=%s" % (EmpID))
            conn.commit()
            resp = jsonify(message='user deleted successfully')
            resp.status_code = 200
            return resp

@cross_origin()
@app.route('/notification_insert', methods=['POST'])
def get_notification_insert():
        '''if request.method == 'POST' and 'user_id' in request.values and 'search_hst' in request.values and 'filepath' in request.values:
            user_id = request.values['user_id']
            search_hst = request.values['search_hst']
            filepath = request.values['filepath']'''
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        search_hst = data['search_hst']
        filepath = data['filepath']
        sql = 'insert into usr_notification(`id`, `user_id`, `search_hst`,`filepath`) values(NULL, %s, %s, %s)'
        values = (user_id, search_hst,filepath)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="notified succesfully")


@cross_origin()
@app.route('/usr_search_history', methods=['POST'])
def get_usr_search_history():
        '''if request.method == 'POST' and 'user_id' in request.values and 'search_history' in request.values and 'filepath' in request.values:
            user_id = request.values['user_id']
            search_history = request.values['search_history']
            filepath = request.values['filepath']'''
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        search_history = data['search_history']
        filepath = data['filepath']
        sql = 'insert into usr_search_history(`id`, `user_id`, `search_history`,`filepath`) values(NULL, %s, %s, %s)'
        values = (user_id, search_history,filepath)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="history added successfully id = "+user_id)

@cross_origin()
@app.route('/my_library_insert', methods =['POST'])
def get_my_fav_insert():
        '''if request.method == 'POST' and 'user_id' in request.values and 'my_fav' in request.values and 'filepath' in request.values and 'SOURCE' in request.values and 'DESCRIPTION' in request.values and 'FILENAME' in request.values :
            user_id = request.values['user_id']
            my_fav = request.values['my_fav']
            filepath = request.values['filepath']
            SOURCE = request.values['SOURCE']
            DESCRIPTION = request.values['DESCRIPTION']
            FILENAME = request.values['FILENAME']'''
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        my_fav = data['my_fav']
        filepath = data['filepath']
        SOURCE = data['SOURCE']
        DESCRIPTION = data['DESCRIPTION']
        FILENAME = data['FILENAME']
        print(user_id)
        print(my_fav)
        sql = 'insert into usr_fav(`id`, `user_id`, `my_fav`,`filepath`,`SOURCE`, `DESCRIPTION`, `FILENAME`) values(NULL, %s, %s, %s, %s, %s, %s)'
        values= (user_id,my_fav,filepath,SOURCE,DESCRIPTION,FILENAME)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql,values)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        return jsonify(message="bookmarked succesfully")

@app.route('/all_notification',methods=['GET'])
def get_all_notification():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from usr_notification")
            conn.commit()
            row = cursor.fetchall()
            #users.append(row)
            #combine_arr = {**mydictionary_users}
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('usr_notification not fou nd',500)
            return resp
        else:
            resp = jsonify('no country found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print('all_notification',e)
    finally:
        cursor.close()
        conn.close()

@app.route("/onclick_notification",methods=['POST'])
def get_onclick_notification():
    if request.method == 'POST' and 'FILENAME' in request.form:
        FILENAME = request.form['FILENAME']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print('FILENAME  ',FILENAME)
        FILENAME_match=''
        sql = "SELECT * FROM `usr_notification` WHERE FILENAME=%s"
        cursor.execute(sql, FILENAME)
        row = cursor.fetchall()
        print(row)
        row = json.loads(row)
        print(row[''])
        if row==0:
            resp = jsonify(row)
            conn.commit()
            resp.status_code = 200
            return jsonify(message="filename in noti db", true='false')
        else:
            return jsonify(message="filename not found in noti db", true='true')

        '''try:
            sql = "SELECT * FROM `usr_notification` WHERE FILENAME=%s"
            values = (FILENAME)
            cursor.execute(sql, FILENAME)
            row = cursor.fetchall()
            print(row)
            email_match = row['7']
            print('FILENAME match',email_match)
            if email_match == FILENAME:
                resp = jsonify(row)
                conn.commit()
                resp.status_code = 200
                return jsonify(message="notification in db",true='false')
            else:
                resp = jsonify(row)
                resp.status_code = 500
                return jsonify(message="notification not exist in db",error='true')
        except Exception as e:
            print(e)
            print('notification result not found')
            return jsonify(message='notification does not exist in db')
        finally:
            cursor.close()
            conn.close()'''

@app.route('/admin_all_user',methods=['GET'])
def admin_all_user():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from registration")
            row = cursor.fetchall()
            #users.append(row)
            #combine_arr = {**mydictionary_users}
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('admin_all_user not found',500)
            return resp
        else:
            resp = jsonify('no country found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print('admin_all_user',e)
    finally:
        cursor.close()
        conn.close()


@app.route('/filter_wise_nptel',methods=['POST'])
def filter_wise_nptel():
    '''data = request.get_json()
    print(data)
    csearch = data['csearch']
    filetype = data['filetype']
    disciplineName = data['disciplineName']
    subjectName = data['subjectName']
    coordinators = data['coordinators']
    institute = data['institute']'''
    csearch = request.form.get("csearch")
    filetype = request.form.get("filetype")
    disciplineName = request.form.get("disciplineName")
    subjectName = request.form.get("subjectName")
    institute = request.form.get("institute")
    coordinators = request.form.get("coordinators")
    data=''
    if csearch:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM `child_real` WHERE lect_name LIKE\"%" + csearch + "%\" AND disciplineName LIKE \"%" + disciplineName + "%\" AND subjectName LIKE \"%" + subjectName + "%\" AND institute LIKE\"%" + institute + "%\" AND filetype LIKE \"%" + filetype + "%\" AND coordinators LIKE \"%" + coordinators + "%\"")
        testing_rows = cursor.fetchall()
        for row in testing_rows:
            data=row
        resp = jsonify(testing_rows)
        return resp

@app.route('/filter_wise_janes',methods=['POST'])
def filter_wise_janes():
    csearch = request.form.get("csearch")
    country = request.form.get("country")
    section = request.form.get("section")
    general_title = request.form.get("general_title")
    status = request.form.get("status")
    data = ''
    if csearch:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "select * from hand where company LIKE\"%" + csearch + "%\" OR country LIKE \"%" + country + "%\" OR section LIKE \"%" + section + "%\" OR general_title LIKE\"%" + general_title +"%\" OR status like \"%" + status + "%\"")
        testing_rows = cursor.fetchall()
        for row in testing_rows:
            data= row
        resp = jsonify(testing_rows)
        return resp

#JANES FILETER LIST######################################################################################################################################
@app.route('/country',methods=['GET'])
def get_country():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            #cursor.execute("select id,country from hand")
            cursor.execute("select DISTINCT(country) from hand ORDER BY country")
            row = cursor.fetchall()
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('data not found in country',500)
            return resp
        else:
            resp = jsonify('no country found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/status',methods=['GET'])
def get_status():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select DISTINCT(status) from hand ORDER BY status")

            row = cursor.fetchall()
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('data not found in status',500)
            return resp
        else:
            resp = jsonify('no status found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/section',methods=['GET'])
def get_section():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select DISTINCT(section) from hand ORDER BY section")
            row = cursor.fetchall()
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('data not found in section',500)
            return resp
        else:
            resp = jsonify('no section found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/general_title',methods=['GET'])
def get_general_title():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select id,general_title from hand")
            row = cursor.fetchall()
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('data not found in general_title',500)
            return resp
        else:
            resp = jsonify('no general_title found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#JANES WISE FILTER #########################################################################################################################################
@app.route("/country_wise",methods=['POST'])
def country_wise():
    if request.method == 'POST' and 'csearch' in request.form and 'country_var' in request.form:
        parser = reqparse.RequestParser()
        csearch = request.form['csearch']
        country_var = request.form['country_var']
        parser.add_argument(country_var, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            #cursor.execute("SELECT * FROM `hand` WHERE country=\""+country_var+"\"")
            cursor.execute("select * from hand where country \"%" + country_var + "%\" AND company LIKE \"%" + csearch + "%\" AND section LIKE \"%" + csearch + "%\" AND general_title LIKE\"%" + csearch + "%\" AND date LIKE \"%" + csearch + "%\" AND status like \"%" + csearch + "%\"")

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

@app.route("/section_wise",methods=['GET', 'POST'])
def section_wise():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        section_var = request.json['section_var']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(section_var, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `hand` WHERE section=\""+section_var+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
            row = cursor.fetchall()
            if not row:
                print("List section is empty")
            resp = jsonify(row)
            resp.status_code = 200
            return jsonify(message="successfully fetched section data!")

        except Exception as e:
            print(e)
            print('section result not found')
        finally:
            cursor.close()
            conn.close()

@app.route("/company_wise",methods=['GET', 'POST'])
def section_company():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        company = request.json['company']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(company, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `hand` WHERE company=\""+company+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
            row = cursor.fetchall()
            if not row:
                print("List company is empty")
            resp = jsonify(row)
            resp.status_code = 200
            return jsonify(message="successfully fetched company data!")

        except Exception as e:
            print(e)
            print('company result not found')
        finally:
            cursor.close()
            conn.close()

@app.route("/general_title_wise",methods=['GET', 'POST'])
def general_title_wise():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        general_title = request.json['general_title']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(general_title, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `hand` WHERE general_title=\""+general_title+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
            row = cursor.fetchall()
            if not row:
                print("List general_title is empty")
            resp = jsonify(row)
            resp.status_code = 200
            return jsonify(message="successfully fetched general_title data!")

        except Exception as e:
            print(e)
            print('general_title result not found')
        finally:
            cursor.close()
            conn.close()

@app.route("/company",methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        company = request.json['company']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(company, type=str)
        args = parser.parse_args()
        print('user section entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `hand` WHERE company=\""+company+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
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
@app.route('/subjectName',methods=['GET', 'POST'])
def get_subjectName():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select DISTINCT(subjectName) from child_real ORDER BY subjectName")
            row = cursor.fetchall()
            resp = jsonify(row)
            if resp.status_code == 200:
                print('success',200)
            elif resp == 500:
                print('data not found',500)
            return resp
        else:
            resp = jsonify('no subjectNames found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/coordinators',methods=['GET', 'POST'])
def get_coordinators():
    conn = None;
    cursor = None;
    try:

        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select DISTINCT(coordinators) from child_real ORDER BY coordinators")
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code
            tus_code = 200
            return resp
        else:
            resp = jsonify('no coordinators found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/institute',methods=['GET', 'POST'])
def get_institute():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            #cursor.execute("select id,institute from child_real ORDER BY institute")
            cursor.execute("select DISTINCT(institute) from child_real ORDER BY institute")
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code
            tus_code = 200
            return resp
        else:
            resp = jsonify('no institutes found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/filetype',methods=['GET', 'POST'])
def get_filetype():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            #cursor.execute("select id,filetype from child_real ORDER BY filetype")
            cursor.execute("select DISTINCT(filetype) from child_real ORDER BY filetype")
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code
            tus_code = 200
            return resp
        else:
            resp = jsonify('no filetype found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/disciplineName',methods=['GET', 'POST'])
def get_disciplineName():
    conn = None;
    cursor = None;
    try:
        if id:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            #cursor.execute("select id,disciplineName from child_real ORDER BY disciplineName")
            cursor.execute("select DISTINCT(disciplineName) from child_real ORDER BY disciplineName")
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('no disciplineNames found')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#NPTEL FILTER WISE LIST #########################################################################################################################################
@app.route("/coordinators_id",methods=['GET', 'POST'])
def coordinators_id():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        coordinator = request.json['coordinator']
        #coordinator = 'Dr. Liza Das'
        parser.add_argument(coordinator, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # inserting the values into the table
            cursor.execute(
                "SELECT * FROM `child_real` WHERE coordinators=\""+coordinator+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
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

@app.route("/subjectName_id",methods=['GET', 'POST'])
def subjectName_id():
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
                "SELECT * FROM `child_real` WHERE subjectName=\""+subjectName+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
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

@app.route("/disciplineName_id",methods=['GET', 'POST'])
def disciplineName_id():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        disciplineName = request.json['disciplineName']
        parser.add_argument(disciplineName, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM `child_real` WHERE disciplineName=\""+disciplineName+"\"")
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

@app.route("/filetype_id",methods=['GET', 'POST'])
def filetype_id():
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
                "SELECT * FROM `child_real` WHERE filetype=\""+filetype+"\"")
                #"select * from child_real where coordinators=%s;"%user)
                #"select p.*,c.* from child_real p inner join child_real c on p.id=c.id where p.coordinators='Dr. Liza Das'")
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

@app.route("/institute_id",methods=['GET', 'POST'])
def institute_id():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        institute = request.json['institute']
        parser.add_argument(institute, type=str)
        args = parser.parse_args()
        print('user coordinator entered : -', args)

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM `child_real` WHERE institute=\""+institute+"\"")
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

@app.route("/email_exist",methods=['POST'])
def email_exist():
    if request.method == 'POST' and 'EMAIL_ID' in request.form:
        EMAIL_ID = request.form['EMAIL_ID']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print('EMAIL_ID ',EMAIL_ID)
        email_match=''
        try:
            sql = "SELECT * FROM `registration` WHERE EMAIL_ID=%s"
            values = EMAIL_ID
            cursor.execute(sql, values)
            row = cursor.fetchone()
            print(row)
            email_match = row['EMAIL_ID']
            if email_match == EMAIL_ID:
                resp = jsonify(row)
                conn.commit()
                resp.status_code = 200
                return jsonify(message="email exist in db",true='false')
            else:
                resp = jsonify(row)
                resp.status_code = 500
                return jsonify(message="email not exist in db",error='true')
        except Exception as e:
            print(e)
            print('email_exist result not found')
            return jsonify(message='email does not exist in db')
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
   app.run(debug=True)
   CORS(app)


