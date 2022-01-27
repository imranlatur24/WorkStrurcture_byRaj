from bs4 import BeautifulSoup
import mysql.connector

try:
    testing_conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        db="wordpress"
    )
    print("wordpress database connected")
    cursor = testing_conn.cursor()
except ConnectionRefusedError:
    print("please check your wordpress server is on")
except:
    print("connection problem in wordpress database")
SOURCE='armablog'
try:
    cursor.execute("select es_sent_subject,es_sent_preview from wp_es_sentdetails")
    data = cursor.fetchall()
    for row in data:
        res = ','.join([''.join(sub) for sub in row])
        soup = BeautifulSoup(res,'lxml')
        for link in soup.findAll('a'):
            print(link.string)

    cursor.execute("select es_sent_subject from wp_es_sentdetails")
    data = cursor.fetchall()
    for es_sent_subject in data:
        convert_str = ', '.join([''.join(sub) for sub in es_sent_subject])
        print(convert_str)
except:
    pass

#ref by https://stackoverflow.com/questions/45900619/extract-link-and-text-if-certain-strings-are-found-beautifulsoup
