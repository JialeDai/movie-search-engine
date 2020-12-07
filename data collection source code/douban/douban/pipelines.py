# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy import settings
from .settings import MONGOD_URL,MONGODB_HOST,MONGODB_PORT,MONGODB_DBNAME,MONGODB_COLNAME
import pymongo
class DoubanPipeline(object):
    def __init__(self):
        self.host = MONGODB_HOST
        self.port = MONGODB_HOST
        self.mongodburl = MONGOD_URL
        self.mongodbname = MONGODB_DBNAME
        self.mongocolname = MONGODB_COLNAME

    def process_item(self,item,spider):
         # 创建mongodb客户端连接对象，该例从settings.py文件里面获取mongodb所在的主机和端口参数，可直接书写主机和端口
        self.client = pymongo.MongoClient(self.mongodburl)
        # 创建数据库douban
        self.mydb = self.client[self.mongodbname]
        # 在数据库douban里面创建表doubanmovies
        self.mycol = self.mydb[self.mongocolname]
        # 把类似字典的数据转换为phthon字典格式
        content = dict(item)
        # 把数据添加到表里面
        self.mycol.insert(content)
        return item