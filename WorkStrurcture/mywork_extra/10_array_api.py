import pymysql
from config.app import app
from db import mysql
from flask import jsonify, request

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
