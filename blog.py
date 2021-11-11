# blog.py

""" Basic blog using webpy 0.3 """
import web
import model
import sys

### Url mappings

urls = (
    "/",
    "Index",
    "/view/(\d+)",
    "View",
    "/new",
    "New",
    "/delete/(\d+)",
    "Delete",
    "/edit/(\d+)",
    "Edit",
    "/graph",
    "Graph"
)


### Templates
t_globals = {"datestr": web.datestr}
render = web.template.render("templates", base="base_trade", globals=t_globals)


class Index:
    def GET(self):
        """ Show page """
        posts = model.get_posts()
        return render.index(posts)


class View:
    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)

class Clear:
    form = web.form.Form(
        web.form.Textbox("title", web.form.notnull, size=30, description="Graph:"))



class New:

    form = web.form.Form(
        web.form.Textbox("title", web.form.notnull, size=30, description="Post title:"),
        web.form.Textarea(
            "content", web.form.notnull, rows=30, cols=80, description="Post content:"
        ),
        web.form.Button("Post entry"),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother("/")


class Delete:
    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother("/")


class Edit:
    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother("/")

class Graph:
    def GET(self):
        form = Clear.form()
        return render.graph(form)

    def POST(self):
        # form = Index.form()
        # post = model.get_post(int(id))
        # if not form.validates():
        raise web.seeother("/")
        # return render.print_graph(form)
        # model.update_post(int(id), form.d.title, form.d.content)
        # raise web.seeother("/")


app = web.application(urls, globals())
sys.argv = ['blog.py', '8007']

if __name__ == "__main__":
    app.run()
    