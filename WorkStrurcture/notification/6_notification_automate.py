#1.in this file we are sending notification against client id
#2.we are sending noti on the basis on user search history tbl
#3.currently we are sending notification on the basis of dspace tbl
#4.dspace tbl data srapped every 24 hrs
#4.other tbl data will be srapped munuel
#6.whenever manual data scrapping is done then automatically notification sent to user but first
#7.uncomment structure like nptel/libsys and so on
#8.notification work is completed here
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
from app import app
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import logging.config



'''logging.basicConfig(
    filename='notification.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')'''
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)
logging.info('Welcome To Intelligent Library Managment System')
logging.info('database connection initializing')
# from register_drdo_db import mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testing'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
logging.info('database connection established')
#@app.route('/notification_insert', methods=['GET'])
def mydata(each):
    with app.app_context():
        search_data = str(each['search_history'])
        EMPID = str(each['EmpID'])
        MARK = "FALSE"
        print('search_keyword ', str(search_data))
        print('EMPID     ', str(EMPID))
        print('MARK     ', MARK)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        mydictionary_dsapce = {}
        mydictionary_dsapce["usearch"] = []
        dspace = mydictionary_dsapce["usearch"]
        # try:
        cursor.execute("select * from dspace WHERE TITLE LIKE %s", ("%" + search_data,))
        dspace_rows = cursor.fetchall()
        for row in dspace_rows:
            print('row ', row)
            dspace.append(row)
            id = row.get('id')
            FILEPATH = str(row.get('filepath'))
            SOURCE = str(row.get('SOURCE'))
            DESCRIPTION = str(row.get('DESCRIPTION'))
            TITLE_dspace = str(row.get('TITLE'))
            print('id',id)
            print('FILEPATH',FILEPATH)
            print('SOURCE',SOURCE)
            print('DESCRIPTION',DESCRIPTION)
            print('TITLE_dspace',TITLE_dspace)

            sql = 'INSERT INTO `usr_notification`(`EmpID`,`search_hst`, `FILEPATH`, `SOURCE`, `DESCRIPTION`, `mark`) VALUES (%s,%s, %s, %s,%s,%s)'
            values = (EMPID, TITLE_dspace, FILEPATH, SOURCE, DESCRIPTION, MARK)
            cursor.execute(sql, values)
            conn.commit()
            print(cursor.rowcount, "record inserted.")
        combine_arr = {**mydictionary_dsapce}
        resp = jsonify(combine_arr)
        return resp
def notification_insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select *from usr_search_history'
    cursor.execute(sql)
    data = cursor.fetchall()
    data_int =  len(data)
    #print('data ',data)
    if data_int == 0:
        print('data not found in usr_search_history tbl')
    else:
        for each in data:
            print('each ',each)
            print(mydata(each))
notification_insert()

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='128.9.32.52')

    CORS(app)