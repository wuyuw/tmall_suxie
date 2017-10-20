# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient


class Tmall2Pipeline(object):
    def open_spider(self, spider):
        host = settings["MONGO_HOST"]
        port = settings["MONGO_PORT"]
        db = settings["DB"]
        collection = settings["COLLECTION"]
        con = MongoClient(host=host, port=port)
        self.collection = con[db][collection]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
