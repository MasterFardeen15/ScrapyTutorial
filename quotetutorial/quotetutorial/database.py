#Testing & practice file
#Not used

import sqlite3


conn = sqlite3.connect("myquotes.db")
curr = conn.cursor()

cmd1 = """CREATE TABLE IF NOT EXISTS quotes_tb(title TEXT, author TEXT, tag TEXT)"""

curr.execute(cmd1)

cmd2 = "INSERT INTO quotes_tb VALUES ('atitle', 'aAuthor', 'aTag')"

curr.execute(cmd2)

# curr.execute("""CREATE TABLE quotes_tb(
#                 title text,
#                 author text,
#                 tag text
#                 )""")


# curr.execute("""INSERT INTO quotes_tb VALUES ('Python is good', 'myname', 'end')""")
    

# curr.execute("""INSERT INTO quotes_tb (title, author, tag) VALUES (?,?,?)""", (
#             item['title'][0],
#             item['author'][0],
#             item['tag'][0]
#         ))
conn.commit()
conn.close()
