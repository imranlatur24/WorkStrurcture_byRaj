import mysql.connector
import psycopg2
try:
    dconn = psycopg2.connect(database="dspace",
                             user="postgres",
                             password="postgres",
                             host="127.0.0.1",
                             port="5432")
    print("postgres database connected")
except:
    print("please check your dspace server is on")
dspace_cur = dconn.cursor()
#creating connection for libsys demo db
try:
    libsys_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="libsys"
    )
    print("libsys database connected")
except ConnectionRefusedError:
    print("make sure your libsys server is on")
except:
    print("connection problem in libsys database")
#creating connection for armablog demo db
try:
    armablog_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="wordpress"
    )
    print("armablog database connected")
except ConnectionRefusedError:
    print("please check your armalog server is on")
except:
    print("connectino problem in armalog database")
#----------------------------------------------
#creating connection for np demo db
try:
    nptel_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="np"
    )
    print("nptel database connected")
except ConnectionRefusedError:
    print("please check you nptel database connection")
except:
    print("connection problem in nptel database")
#----------------------------------------------
#creating connection for armablog demo db
try:
    janes_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="janes"
    )
    print("janes database connected")
except ConnectionRefusedError:
    print("please check your janes database connection")
except:
    print("connection problem in janes database")
#----------------------------------------------
#common db
try:
    common_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="common_db"
    )
    common_cur = common_conn.cursor()
    print("common database connected")
except ConnectionRefusedError:
    print("please check your common database connection")
except:
    print("connection problem in common database")
#----------------------------------------------
try:
    dspace_cur.execute("select metadata_value_id,resource_id,metadata_field_id,text_value,place,resource_type_id from metadatavalue")
    meta = dspace_cur.fetchall()
    for row in meta:
        print('fetched ',row);
        metadata_value_id = str(row[0])
        resource_id = str(row[1])
        metadata_field_id = str(row[2])
        text_value = str(row[3])
        place = str(row[4])
        resource_type_id = str(row[5])
        print(metadata_field_id)
        print(resource_id)
        print(text_value)
        print(place)
        print(resource_type_id)
        sql = "INSERT INTO dspace VALUES(%s ,%s, %s, %s, %s ,%s)"
        val = (metadata_value_id,
            resource_id,
            metadata_field_id,
            text_value,
            place,
            resource_type_id)
        common_cur.execute(sql, val)
        common_conn.commit()
except:
    dconn.rollback()
dconn.close()

try:
    libsys_cur = libsys_conn.cursor()
    libsys_cur.execute("SELECT LIB_ID,"
                       " BUDGT_YEAR,"
                       " BUDGT_HEAD,"
                       " BUDGT_YEAR_ALT,"
                       " BUDGT_HEAD_NAME,"
                       " BUDGT_APPRVD,"
                       " ORDERED_AMT,"
                       " BILLED_AMT,"
                       " NUM_SRLS_APPRVD,"
                       " NUM_SRLS_ORDERD,"
                       " NUM_SRLS_BILLED,"
                       " BILLED_AMT_PREV_YEAR,"
                       " NUM_SRLS_PREV_YEAR,"
                       " FILLER1,"
                       " MAIN_KEY,"
                       " BUDGET_ALT_KEY,"
                       " BUDGET_TYPE,"
                       " DEPT_BUDGT,"
                       " ACCT_CODE,"
                       " CURR_BALANCE_FAIS"
                       " from BUDGET_TBL")
    rows = libsys_cur.fetchall()
    for row in rows:
        LIB_ID = str(row[0])
        BUDGT_YEAR = str(row[1])
        BUDGT_HEAD = str(row[2])
        BUDGT_YEAR_ALT = str(row[3])
        BUDGT_HEAD_NAME = str(row[4])
        BUDGT_APPRVD = str(row[5])
        ORDERED_AMT = str(row[6])
        BILLED_AMT = str(row[7])
        NUM_SRLS_APPRVD = str(row[8])
        NUM_SRLS_ORDERD = str(row[9])
        NUM_SRLS_BILLED = str(row[10])
        BILLED_AMT_PREV_YEAR = str(row[11])
        NUM_SRLS_PREV_YEAR = str(row[12])
        FILLER1 = str(row[13])
        MAIN_KEY = str(row[14])
        BUDGET_ALT_KEY = str(row[15])
        BUDGET_TYPE = str(row[16])
        DEPT_BUDGT = str(row[17])
        ACCT_CODE = str(row[18])
        CURR_BALANCE_FAIS = str(row[19])
        print("LIB_ID = ",LIB_ID)
        print("BUDGT_YEAR = ",BUDGT_YEAR)
        print("BUDGT_HEAD = ",BUDGT_HEAD)
        print("BUDGT_YEAR_ALT = ",BUDGT_YEAR_ALT)
        print("BUDGT_HEAD_NAME = ",BUDGT_HEAD_NAME)
        print("BUDGT_APPRVD = ",BUDGT_APPRVD)
        print("ORDERED_AMT = ",ORDERED_AMT)
        print("BILLED_AMT = ",BILLED_AMT)
        print("NUM_SRLS_APPRVD = ",NUM_SRLS_APPRVD)
        print("NUM_SRLS_ORDERD = ",NUM_SRLS_ORDERD)
        print("NUM_SRLS_BILLED = ",NUM_SRLS_BILLED)
        print("BILLED_AMT_PREV_YEAR = ",BILLED_AMT_PREV_YEAR)
        print("NUM_SRLS_PREV_YEAR = ",NUM_SRLS_PREV_YEAR)
        print("FILLER1 = ",FILLER1)
        print("MAIN_KEY = ",MAIN_KEY)
        print("BUDGET_ALT_KEY = ",BUDGET_ALT_KEY)
        print("BUDGET_TYPE = ",BUDGET_TYPE)
        print("DEPT_BUDGT = ",DEPT_BUDGT)
        print("ACCT_CODE = ",ACCT_CODE)
        print("CURR_BALANCE_FAIS = ",CURR_BALANCE_FAIS)

        sql = "INSERT INTO lib VALUES(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (LIB_ID,
               BUDGT_YEAR,
               BUDGT_HEAD,
               BUDGT_YEAR_ALT,
               BUDGT_HEAD_NAME,
               BUDGT_APPRVD,
               ORDERED_AMT,
               BILLED_AMT,
               NUM_SRLS_APPRVD,
               NUM_SRLS_ORDERD,
               NUM_SRLS_BILLED,
               BILLED_AMT_PREV_YEAR,
               NUM_SRLS_PREV_YEAR,
               FILLER1,
               MAIN_KEY,
               BUDGET_ALT_KEY,
               BUDGET_TYPE,
               DEPT_BUDGT,
               ACCT_CODE,
               CURR_BALANCE_FAIS)

        common_cur.execute(sql, val)
        common_conn.commit()
except:
    libsys_conn.rollback()
libsys_conn.close()

#----------------------------------------------
#creating armablog cursor
try:
    armablog_cur = armablog_conn.cursor()
    armablog_cur.execute("select comment_ID,comment_post_ID,comment_author,comment_author_email,comment_author_url,"
                         "comment_author_IP,comment_date,comment_date_gmt,comment_content,comment_karma,comment_approved,"
                         "comment_agent,comment_type,comment_parent,user_id from wp_comments")
    rows = armablog_cur.fetchall()
    for row in rows:
        comment_ID = str(row[0])
        comment_post_ID = str(row[1])
        comment_author = str(row[2])
        comment_author_email = str(row[3])
        comment_author_url = str(row[4])
        comment_author_IP = str(row[5])
        comment_date = str(row[6])
        comment_date_gmt = str(row[7])
        comment_content = str(row[8])
        comment_karma = str(row[9])
        comment_agent = str(row[10])
        comment_type = str(row[11])
        comment_approved = str(row[12])
        comment_parent = str(row[13])
        user_id = str(row[14])
        print("comment_ID = ",comment_ID)
        print("comment_post_ID = ",comment_post_ID)
        print("comment_author = ",comment_author)
        print("comment_author_email = ",comment_author_email)
        print("comment_author_url = ",comment_author_url)
        print("comment_author_IP = ",comment_author_IP)
        print("comment_date = ",comment_date)
        print("comment_date_gmt = ",comment_date_gmt)
        print("comment_content = ",comment_content)
        print("comment_karma = ",comment_karma)
        print("comment_approved = ",comment_approved)
        print("comment_agent = ",comment_agent)
        print("comment_type = ",comment_type)
        print("comment_parent = ",comment_parent)
        print("user_id = ",user_id)


        sql = "INSERT INTO wp_comments VALUES(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (comment_ID,comment_post_ID,comment_author,comment_author_email,comment_author_url,comment_author_IP,comment_date,comment_date_gmt,
               comment_content,comment_karma,comment_approved,comment_agent,comment_type,comment_parent,user_id)
        common_cur.execute(sql, val)
        common_conn.commit()
except:
    armablog_conn.rollback()
armablog_conn.close()

#creating janes cursor
try:
    janes_cur = janes_conn.cursor()
    janes_cur.execute("select company,country,section,general_title,date,status,filepath,keyword_1,keyword_2,keyword_3 from hand")
    rows = janes_cur.fetchall()
    #print(rows)
    num = 0
    #fetching janes data from janes db to common db
    for row in rows:
        Company = str(row[0])
        Country = str(row[1])
        Section = str(row[2])
        title = str(row[3])
        date_conv = str(row[4])
        UpdateStatus = str(row[5])
        file_path = str(row[6])
        keyword_1 = str(row[7])
        keyword_2 = str(row[8])
        keyword_3 = str(row[9])
        print("Company = ",Company)
        print("Country = ",Country)
        print("Section = ",Section)
        print("title = ",title)
        print("date_conv = ",date_conv)
        print("UpdateStatus = ",UpdateStatus)
        print("file_path = ",file_path)
        sql = "INSERT INTO hand VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (num, Company, Country, Section, title, date_conv, UpdateStatus, file_path, keyword_1, keyword_2,keyword_3)
        # inserting the values into the table
        common_cur.execute(sql, val)
        #num = num + 1
        # commit the transaction
        common_conn.commit()
except:
    janes_conn.rollback()
janes_conn.close()

#creating nptel cursor
try:
    nptel_cur = nptel_conn.cursor()
    nptel_cur.execute("select id,subject_id,disciplineName,subjectName,coordinators,filetype,institute,filename,filepath,keyword_1,keyword_2,keyword_3 from nptel")
    rows = nptel_cur.fetchall()
    id = 0
    for row in rows:
        subject_id = str(row[1])
        disciplineName = str(row[2])
        subjectName = str(row[3])
        coordinators = str(row[4])
        filetype = str(row[5])
        institute = str(row[6])
        filename = str(row[7])
        filepath = str(row[8])
        keyword_1 = str(row[9])
        keyword_2 = str(row[10])
        keyword_3 = str(row[11])
        print("subject_id = ",subject_id)
        print("disciplineName = ",disciplineName)
        print("subjectName = ",subjectName)
        print("coordinators = ",coordinators)
        print("filetype = ",filetype)
        print("institute = ",institute)
        print("filename = ",filename)
        print("filepath = ",filepath)
        print("keyword_1 = ",keyword_1)
        print("keyword_2 = ",keyword_2)
        print("keyword_3 = ",keyword_3)

        sql = "INSERT INTO parent VALUES(%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id,subject_id,disciplineName,subjectName,coordinators,filetype,institute,filename,filepath,"","","")
        common_cur.execute(sql, val)
        common_conn.commit()
except:
    nptel_conn.rollback()
nptel_conn.close()

