# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors

class CollectipsPipeline(object):
    def process_item(self, item, spider):
        # # 打开数据库连接
        # db = pymysql.connect("localhost", "root", "password", "testdb")
        #
        # # 使用 cursor() 方法创建一个游标对象 cursor
        # cursor = db.cursor()
        #
        # # 使用 execute() 方法执行 SQL，如果表存在则删除
        # cursor.execute("DROP TABLE IF EXISTS COLLECTIPS")
        #
        # # SQL 插入语句
        # sql = "INSERT INTO COLLECTIPS(IP,PORT,TYPE,POSITION,SPEED,LAST_CHECK_TIME)" \
        #       "VALUES (%s, %s,  %s,  %s,  %s, %s)" % \
        #       (item['IP'], item['PORT'], item['TYPE'], item['POSITION'], item['SPEED'], item['LAST_CHECK_TIME'])
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 执行sql语句
        #     db.commit()
        # except:
        #     # 发生错误时回滚
        #     db.rollback()
        #
        # # 关闭数据库连接
        # db.close()

        # cur = con.cursor()
        # sql = ("insert into proxy(IP,PORT,TYPE,POSITION,SPEED,LAST_CHECK_TIME)"
        #        "values(%s,%s,%s,%s,%s,%s)")
        # lis = (item['IP'],item['PORT'],item['TYPE'],item['POSITION'],item['SPEED'],item['LAST_CHECK_TIME'])
        # try:
        #     cur.execute(sql,lis)
        # except Exception as e:
        #     print(e)
        #     con.rollback()
        # else:
        #     con.commit()
        # cur.close()
        # con.close()

        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root123',
            db='ip_poxies',
            charset='utf8')

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = connect.cursor()

        # SQL 插入语句
        sql = "INSERT INTO iplist (ip, port, address, anony, speed, time) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s')"
        lis = (item['IP'], item['PORT'], item['TYPE'], item['POSITION'], item['SPEED'], item['LAST_CHECK_TIME'])
        try:
            # 执行sql语句
            cursor.execute(sql % lis)
            # 执行sql语句
            connect.commit()
        except:
            # 发生错误时回滚
            connect.rollback()
        # 关闭连接
        cursor.close()
        connect.close()
        return item
