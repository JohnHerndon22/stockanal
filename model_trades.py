#model.py

import web, datetime

db = web.database(dbn="mysql", db="trading", user="root", password="Sushiman12.")

def get_parms():
    return db.select("game_parameters", order="game_id")

def get_orders():
    return db.select("orders", order="order_id")


def get_post(id):
    try:
        return db.select("entries", where="id=$id", vars=locals())[0]
    except IndexError:
        return None


def next_day(title):
    print(title)
    return 

def del_post(id):
    db.delete("entries", where="id=$id", vars=locals())


def update_post(id, title, text):
    db.update("entries", where="id=$id", vars=locals(), title=title, content=text)