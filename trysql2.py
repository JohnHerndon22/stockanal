# trysql2.py

import mysql.connector as ms

cnx = ms.connect(db="trading", user="root", password="Sushiman12.")
cursor = cnx.cursor()

results = cursor.execute('''select * from orders''')
print(results) 

# for result in results:
#     print(result)

quit()