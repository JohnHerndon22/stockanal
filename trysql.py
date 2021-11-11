# trysql.py

import mysql.connector

        # port=5432,
        # host='127.0.0.1',



mydb = mysql.connector.connect(user="root", password="Sushiman12.",
        host="127.0.0.1",
        database="testdb")

# mydb = mysql.connector.connect(user="root", passwd="",
#         host="localhost",
#         database="dbname")

# conn = mysql.connector.connect(
#     user='root', password='password', host='127.0.0.1', database='mydb'
# )

#Creating a cursor object using the cursor() method
cursor = mydb.cursor()

#Dropping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS todo")

sql ='''CREATE TABLE todo (
    id serial primary key,
    title text,
    created timestamp default now(),
    done boolean default 'f'
)'''
cursor.execute(sql)

cursor.close()
