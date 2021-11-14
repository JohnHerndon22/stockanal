import web

db = web.database(dbn="mysql", db="trading", user="root", password="Sushiman12.")

results = db.query("SELECT MAX(game_id) AS high_game_id FROM game_parameters ORDER BY game_id")

for row in results:
    # print(row['high_game_id'])
    new_high_id = row['high_game_id']

new_high_id+=1
# print(new_high_id)


db.insert('game_parameters', game_id=new_high_id, _test=False)


new_results = db.query("SELECT MAX(game_id) AS high_game_id FROM game_parameters ORDER BY game_id")
print(new_results[0].high_game_id)
