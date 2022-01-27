import mysql.connector
from flask import jsonify
from flask_cors import CORS
from app import app
import pymysql


try:
    testing_conn = mysql.connector.connect(
        host="database-2.cwnpl8w0h65y.us-east-1.rds.amazonaws.com",
        user="novetrics",
        password="novetrics123")
    print("novetrics database connected")
    testing_cursor = testing_conn.cursor()
except ConnectionRefusedError:
    print("please check your novetrics server is on")
except:
    print("connection problem in novetrics database")

'''testing_cursor.execute("SELECT VERSION()")
data = testing_cursor.fetchone()
print(data)'''
@app.route('/common_db', methods=['GET'])
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

        '''mydictionary_dspace = {}
        mydictionary_dspace["dspace"] = []
        dspace = mydictionary_dspace["dspace"]'''
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

            ''' cursor.execute("SELECT * FROM dspace WHERE text_value LIKE\"%"+ csearch + "%\"")
            metadatavalue_janes = cursor.fetchall()
            for jrow in metadatavalue_janes:
                dspace.append(jrow)'''

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
        conn.close()

if __name__ == "__main__":
   app.run(debug=True)
   CORS(app)


