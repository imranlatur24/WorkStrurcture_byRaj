#1.get last record from armablog_title ex.255
#2.get last record from armablog_filepath ex.255
#3.then we are comparing both tables record and then
#4.we are updating or merge both tables data into 3rd table data which is name is armablog_filepath or armablog_filepath2
#5.we are performing search operation on armablog_filepath or armablog_filepath2 table means our arma process is completed here
import mysql.connector
import logging

logging.basicConfig(
    filename='armablog_merge.log',
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
logging.info('armablog merge file calling here')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.warning('testing db connection is establishing in ARMABLOG_MERGE')
try:
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      password="",
      database="testing"
    )
    mycursor = mydb.cursor()
    print('testing db connected')
    print('cursor connected')
    logging.debug('testing amrablog merge file db connected')
except:
    print('testing db not connected')
    logging.debug('testing amrablog merge file db connected')


try:
    # fetch id from child_lectname

    mycursor.execute('SELECT id FROM armablog_title ORDER BY id DESC LIMIT 1')
    limit_lectname = mycursor.fetchone()
    lectName = limit_lectname[0]
    logging.debug('armablog_title length in amrablog merge file ',lectName)
    print('armablog title size ',lectName)
    # fetch id from child_real(lect_path)
    mycursor.execute('SELECT id FROM armablog_filepath ORDER BY id DESC LIMIT 1')
    limit_lectpath = mycursor.fetchone()
    lectPath = limit_lectpath[0]
    logging.debug('armablog_filepath length in amrablog merge file ',lectPath)
    print('armablog filepath size ',lectPath)
    if lectName == lectPath:
        for i in range(lectPath):
            # increment value from 0=1
            j = i + 1
            # sql=cursor.execute('UPDATE merge SET lect_name=%s WHERE id=%s;')
            sql_childlect = mycursor.execute('SELECT TITLE FROM armablog_title where id=%s;' % j)
            succ_childlect = mycursor.fetchone()
            str_succ_childlect = str(succ_childlect[0])
            print(str_succ_childlect)
            #updating each record
            sql = "UPDATE armablog_filepath SET TITLE = %s WHERE id= %s"
            print(j)
            val_merge = (str_succ_childlect, j)
            mycursor.execute(sql, val_merge)
            #mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
    elif lectName == lectPath:
        print('armablog_title and-or armablog_filepath is not matched')
        logging.warning('armablog_title and-or armablog_filepath is not matched ')
except TypeError:
    print('your armablog_title or armablog_filepath table is empty')
    logging.warning('your armablog_title or armablog_filepath table is empty')
    logging.warning('armablog merge file work is completed')
finally:
    mycursor.execute(
        'DELETE n1 FROM armablog_filepath n1, armablog_filepath n2 WHERE n1.id > n2.id AND n1.TITLE = n2.TITLE')
    mycursor.execute("delete from armablog_filepath where TITLE=''")
    mycursor.execute("UPDATE armablog_filepath SET filepath= REPLACE(filepath,'http://128.9.24.131/wordpress','https://128.9.32.52/wordpress');")
    mydb.commit()
    mydb.close()
