import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="8172",   # apna password
    database="school_management",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()