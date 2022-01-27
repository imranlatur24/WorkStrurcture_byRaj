## make sure your libsys table should be UNIQUE value for FILENAME column

#1.in this file we are fetching multiple columns data from libsys db which is exisiting db in drdo and it is available into mysql
#2.all columns data we managed into testing/drdo db which is
#3.libsys work is completed here.
#4.we are performing search operation here
import logging
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(
    filename='libsys.log',
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
logging.warning('LIBSYS_INSERT_DATA FILE CALLING FOR SCRAPPINGS')
logging.warning('check db connection')
logging.warning('chck db available')
logging.warning('check table available')
logging.warning('check server is on')
logging.warning('if error occured then remove try catch block')
logging.debug('libsys database connection establishing..in LIBSYS INSERT DATA FILE')

import mysql.connector
def sql_conn(hostname,username,password,dbname):
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=dbname,buffered=True)
    ##print('libsys database connected successfully with id 128.9.24.131 and database libsys')
    logging.debug('libsys database connected successfully')
    return conn
def subject_title_tbl():
    logging.debug('libys db connection establishing')
    # conn = sql_conn("128.9.24.131", "libsys", "libsys", "libsys")
    conn = sql_conn("128.9.32.52", "root", "", "libsys")
    logging.debug('LIBSYS db connection established..!')
    cur = conn.cursor()

    cur.execute("select DISTINCT(TITLE_ALT) from subject_title_tbl ORDER BY TITLE_ALT")
    subject_title_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA subject_title_tbl array ',subject_title_tbl)
    cur.execute("select DISTINCT(TITLE_ALT_1) from approval_details_tbl ORDER BY TITLE_ALT_1")
    approval_details_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA approval_details_tbl array ', approval_details_tbl)

    cur.execute("select DISTINCT(TITLE_NAME) from new_arrivals_tbl ORDER BY TITLE_NAME")
    new_arrivals_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA new_arrivals_tbl array ', new_arrivals_tbl)

    cur.execute("select DISTINCT(AUT_ALT_KEY) from subjct_auth_tbl ORDER BY AUT_ALT_KEY")
    subjct_auth_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA new_arrivals_tbl array ', new_arrivals_tbl)

    cur.execute("select DISTINCT(SERIAL_NAME_ALT) from srl_bindery_tbl ORDER BY SERIAL_NAME_ALT")
    srl_bindery_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA new_arrivals_tbl array ', new_arrivals_tbl)

    cur.execute("select DISTINCT(SERIAL_ALT_1) from srl_approval_details_tbl ORDER BY SERIAL_ALT_1")
    srl_approval_details_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA srl_approval_details_tbl array ', srl_approval_details_tbl)

    cur.execute("select DISTINCT(SUBJECT) from srl_special_issues_tbl ORDER BY SUBJECT")
    srl_special_issues_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA srl_special_issues_tbl array ', srl_special_issues_tbl)

    cur.execute("select DISTINCT(ORDER_TITLE_ALT1) from order_details_tbl ORDER BY ORDER_TITLE_ALT1")
    order_details_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA order_details_tbl array ', order_details_tbl)

    cur.execute("select DISTINCT(SHORT_NAME) from srl_serial_receipt_tbl ORDER BY SHORT_NAME")
    srl_serial_receipt_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA srl_serial_receipt_tbl array ', srl_serial_receipt_tbl)

    cur.execute("select DISTINCT(TITLE_NAME) from title_exception_tbl ORDER BY TITLE_NAME")
    title_exception_tbl = cur.fetchall()
    logging.debug('LIBSYS_INSERT_DATA title_exception_tbl array ', title_exception_tbl)

    SOURCE = 'libsys'
    id = 1
    try:
        for i in subject_title_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in title_exception_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in srl_serial_receipt_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in order_details_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in srl_approval_details_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in srl_special_issues_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in srl_bindery_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in approval_details_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in new_arrivals_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()

        for i in subjct_auth_tbl:
            res = ', '.join([''.join(sub) for sub in i])
            sql = "INSERT INTO `libsys`(`id`, `FILENAME`, `SOURCE`) VALUES (null,%s,%s)"
            values = (res, SOURCE)
            print(res)
            id = id + 1
            cur.execute(sql, values)
            print(values)
            conn.commit()
    except:
        conn.rollback()
    print(cur.rowcount, "record inserted ")
    conn.close()

subject_title_tbl()
