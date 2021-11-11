#app.py

import web
from web import form
# import mysqldb
import mysql.connector

render = web.template.render('templates/')


# urls = (
#     "/tasks/?", "signin",
#     "/tasks/list", "listing",
#     "/tasks/post", "post",
#     "/tasks/chgpass", "chgpass",
#     "/tasks/act", "actions",
#     "/tasks/logout", "logout",
#     "/tasks/signup", "signup"
# )

urls = (
    '/(.*)', 'index',
    '/graph', 'graph'
)
app = web.application(urls, globals())

class index:
    def GET(self, name):
        return render.index(name)

# class graph:
#     def POST

if __name__ == "__main__":
    app = web.application(urls, globals())
 
    # mydb = mysql.connector.connect(user="root", password="Sushiman12.",
    #         host="127.0.0.1",
    #         database="testdb")

    # #Creating a cursor object using the cursor() method
    # cursor = mydb.cursor()

    # #Dropping todo table if already exists.
    # cursor.execute("DROP TABLE IF EXISTS todo")

    # sql ='''CREATE TABLE todo (
    #     id serial primary key,
    #     title text,
    #     created timestamp default now()
    #     )'''
    # cursor.execute(sql)

    # sql = '''INSERT INTO todo (title) VALUES ('Learn web.py');'''
    # cursor.execute(sql)

    #Closing the connection
    # conn.close()

    # INSERT INTO todo (title) VALUES ('Learn web.py');

    app.run()