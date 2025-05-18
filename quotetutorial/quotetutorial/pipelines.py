# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

class QuotetutorialPipeline:
    
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['myquotes']
        self.collection = db['quotes_tb']
    
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item




# USING MYSQL

# import mysql.connector

# class QuotetutorialPipeline:
    
#     def __init__(self):
#         self.create_connection()
#         self.create_table()
    
#     def create_connection(self):
#         self.conn = mysql.connector.connect(
#             host = 'localhost',
#             user = 'root',
#             passwd = 'root123',
#             database = 'myquotes'
#         )
#         self.curr = self.conn.cursor()
    
#     def create_table(self):
#         self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
#         self.curr.execute("""CREATE TABLE quotes_tb(
#                             title TEXT,
#                             author TEXT,
#                             tag TEXT
#                             )""")

#     def process_item(self, item, spider):
#         self.store_db(item)
#         print("Pipeline : " + item['title'][0])
#         return item
    
#     def store_db(self, item):
#         adapter = ItemAdapter(item)
#         tag_list = adapter.get('tag', [])
#         tags = ', '.join(tag_list) if isinstance(tag_list, list) else tag_list        
#         self.curr.execute("""INSERT INTO quotes_tb (title, author, tag) VALUES (%s,%s,%s)""", (
#             item['title'][0],
#             item['author'][0],
#             tags
#         ))
#         self.conn.commit()



# USING SQLITE3

# import sqlite3

# class QuotetutorialPipeline:
    
#     def __init__(self):
#         self.create_connection()
#         self.create_table()
    
#     def create_connection(self):
#         self.conn = sqlite3.connect("myquotes.db")
#         self.curr = self.conn.cursor()
    
#     def create_table(self):
#         self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
#         self.curr.execute("""CREATE TABLE quotes_tb(
#                             title TEXT,
#                             author TEXT,
#                             tag TEXT
#                             )""")

#     def process_item(self, item, spider):
#         self.store_db(item)
#         print("Pipeline : " + item['title'][0])
#         return item
    
#     def store_db(self, item):
#         adapter = ItemAdapter(item)
#         # title = adapter.get('title', [''])[0]
#         # author = adapter.get('author', [''])[0]
#         tag_list = adapter.get('tag', [])
#         tags = ', '.join(tag_list) if isinstance(tag_list, list) else tag_list        
#         self.curr.execute("""INSERT INTO quotes_tb (title, author, tag) VALUES (?,?,?)""", (
#             item['title'][0],
#             item['author'][0],
#             tags
#         ))
#         self.conn.commit()

#     # Optional
#     def close_spider(self, spider):
#         self.conn.close()