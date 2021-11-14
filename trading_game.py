# trading_game.py

""" Basic blog using webpy 0.3 """
import web
from web.webapi import SeeOther
import model_trades
import sys

### Url mappings

urls = (
    "/",
    "Index",
    "/newgame",
    "New_Game"
    "/view/(\d+)",
    "View",
    "/nextday",
    "Next_Day",
    "/delete/(\d+)",
    "Delete",
    "/edit/(\d+)",
    "Edit",
    "/endgame",
    "End_Game"
    
)


### Templates and start new game
t_globals = {"datestr": web.datestr}
render = web.template.render("templates", base="base_trade", globals=t_globals)
running_game = False

class Index:
    def GET(self):
        """ Show page """
        if running_game == False:
            raise web.seeother("/newgame")
            # form = web.form.Form(
            #     web.form.Textbox("start_date", web.form.notnull, size=30, description="Start Date"),
            #     web.form.Textbox("end_date", web.form.notnull, size=30, description="End Date"),
            #     web.form.Textbox("symbol", web.form.notnull, size=30, description="Symbol"),
            #     web.form.Textbox("invest_total", web.form.notnull, size=30, description="Invest Total"),
            #     web.form.Button("Start Game"))
            # return render.newgame(form)
        else:
            game_parms = model_trades.get_parms()
        
        orders = model_trades.get_orders()
        return render.index(orders, game_parms)

class View:
    def GET(self, id):
        """ View single post """
        post = model_trades.get_post(int(id))
        return render.view(post)

class Clear:
    form = web.form.Form(
        web.form.Textbox("title", web.form.notnull, size=30, description="Graph:"))



class Next_Day:

    form = web.form.Form(
        web.form.Textbox("title", web.form.notnull, size=30, description="New Day"),
        web.form.Button("Next Day"),
    )

    def GET(self):
        form = self.form()
        return render.nextday(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.nextday(form)
        model_trades.next_day(form.d.title)
        raise web.seeother("/")


class Delete:
    def POST(self, id):
        model_trades.del_post(int(id))
        raise web.seeother("/")


class Edit:
    def GET(self, id):
        post = model_trades.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = model_trades.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model_trades.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother("/")

class End_Game:
    def GET(self):
        form = Clear.form()
        return render.endgame(form)

    def POST(self):
        # form = Index.form()
        # post = model_trades.get_post(int(id))
        # if not form.validates():
        raise web.seeother("/")
        # return render.print_graph(form)
        # model_trades.update_post(int(id), form.d.title, form.d.content)
        # raise web.seeother("/")

class New_Game:
    
    newgame_id = model_trades.insert_new_game()

    form = web.form.Form(
        web.form.Textbox("start_date", web.form.notnull, size=30, description="Start Date"),
        web.form.Textbox("end_date", web.form.notnull, size=30, description="End Date"),
        web.form.Textbox("symbol", web.form.notnull, size=30, description="Symbol"),
        web.form.Textbox("invest_total", web.form.notnull, size=30, description="Invest Total"),
        web.form.Button("Start Game"))
    
    def GET(self):
        return render.newgame(newgame_id, form)

    def POST(self):
        # form = Index.form()
        # post = model_trades.get_post(int(id))
        # if not form.validates():
        # return render.print_graph(form)
        model_trades.update_game_parms(form.start_date, form.end_date, form.symbol, form.invest_total)
        raise web.seeother("/")

app = web.application(urls, globals())
sys.argv = ['trading_game.py', '8006']

if __name__ == "__main__":
    app.run()
    