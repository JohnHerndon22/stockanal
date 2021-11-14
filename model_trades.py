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
    return

def insert_new_game():
    results = db.query("SELECT MAX(game_id) AS high_game_id FROM game_parameters ORDER BY game_id")

    for row in results:
        new_high_id = row['high_game_id']

    new_high_id+=1
    db.insert('game_parameters', game_id=new_high_id, _test=False)

    return new_high_id

def update_game_parms(start_date, end_date, symbol, invest_total):
    # increment next game id
    db.update("game_parameters", where="game_id=$id", vars=locals(), invest_total=invest_total, start_date=start_date, end_date=end_date, symbol=symbol)
    return db.select("game_parameters", order="game_id")