#app.py

import web
from web import form
# import mysqldb

render = web.template.render('templates')

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]
)

urls = (
    '/', 'register'
)
# app = web.application(urls, globals())

class register:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.register(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            return render.register(f)
        else:
            # do whatever is required for display register
            print("registering.....")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
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

    