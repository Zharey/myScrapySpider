# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import copy
from twisted.enterprise import adbapi

class AutocomplaintsPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
                host = settings["MYSQL_HOST"],
                db = settings["MYSQL_DBNAME"],
                user = settings["MYSQL_USER"],
                passwd = settings["MYSQL_PASSWORD"],
                charset = "utf8",
                cursorclass = pymysql.cursors.DictCursor,
                use_unicode = True
            )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        asynItem = copy.deepcopy(item)
        query = self.dbpool.runInteraction(self.do_insert, asynItem)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursors, item):
        insert_sql = """
                        insert into 汽车投诉信息 (投诉品牌,投诉车系,投诉车型,投诉简述,投诉部位,投诉故障,投诉服务,服务问题,投诉时间)
                        value(%s,%s,%s,%s,%s,%s,%s,%s,%s) """

        cursors.execute(insert_sql, (item['tspp'], item['tscx'], item['tscxing'], item['tsjs'], item['tsbw'], item['tswt'], item['tsfw'], item['fwwt'], item['tssj']))
