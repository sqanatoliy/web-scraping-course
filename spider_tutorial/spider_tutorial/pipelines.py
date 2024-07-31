# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
import pymongo
import sqlite3


class MongodbPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://sqanatoliy:sqanatoliy@cluster0.iauexdl.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class SQLitePipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE transcripts (
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcripts (title, plot, transcript, url) VALUES (?, ?, ?, ?)
        ''', (
            item['title'],
            item['plot'],
            item['transcript'],
            item['url'],
        ))
        self.connection.commit()
        return item