#1.get last record from child_lectname ex.255
#2.get last record from child_real ex.255
#3.then we are comparing both tables record and then
#4.we are updating or merge both tables data into 3rd table data which is name is child_real
#5.we are performing search operation on child_real table means our nptel process is completed here
import logging
logging.basicConfig(
    filename='C:/Users/3029/PycharmProjects/WorkStrurcture/WorkStrurcture/logs/merge_filename_nptel.log',
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
logging.info('merge_filename file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('drdo database establishing in merge_filename file')
logging.debug('child_real database connection establishing..in merge_filename FILE')

import mysql.connector
try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="testing"
)
except:
    print('test db not connected')
    logging.log('child_lectname table and child_real table in test db is connnected successfully in child_filepath file')

try:
    # fetch id from child_lectname
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM child_lectname ORDER BY id DESC LIMIT 1')
    limit_lectname = mycursor.fetchone()
    lectName = limit_lectname[0]
    print(lectName)
    # fetch id from child_real(lect_path)
    mycursor.execute('SELECT id FROM child_real ORDER BY id DESC LIMIT 1')
    limit_lectpath = mycursor.fetchone()
    lectPath = limit_lectpath[0]
    print(lectPath)
    if lectName == lectPath:
        SOURCE = 'nptel'
        for i in range(lectPath):
            # increment value from 0=1
            j = i + 1
            # sql=cursor.execute('UPDATE merge SET lect_name=%s WHERE id=%s;')
            sql_childlect = mycursor.execute('SELECT lect_name FROM child_lectname where id=%s;' % j)
            succ_childlect = mycursor.fetchone()
            str_succ_childlect = str(succ_childlect[0])
            print(str_succ_childlect)
            #updating each record
            sql = "UPDATE child_real SET lect_name = %s, TITLE=%s, SOURCE=%s WHERE id= %s"
            print(j)
            val_merge = (str_succ_childlect,str_succ_childlect,SOURCE, j)
            mycursor.execute(sql, val_merge)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
    elif lectName == lectPath:
        ('lectname and-or lectpath is not matched')
except TypeError:
    print('your lectname or lectpath table is empty')

