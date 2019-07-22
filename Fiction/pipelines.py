# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymysql


class FictionPipeline(object):
    def __init__(self):
        # connection database
        self.connect = pymysql.connect('localhost', 'root', '123456', 'test')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        print("开始输入数据")
        try:

            # sql为你的查询语句
            sql = "SELECT id FROM test_novel WHERE `chapter_name` = %s"
            self.cursor.execute(sql, (item["chapter_name"]))
            result = self.cursor.fetchone()

            if result == None:
                self.cursor.execute(
                    "insert into test_novel(chapter_num, `name`, chapter_name, chapter_content) values (%s, %s, %s, %s)",
                    (item['chapter_num'], item['name'], item['chapter_name'], item['chapter_content']))
            else:
                ids = result[0]
                self.cursor.execute(
                    "update test_novel set `name` = %s, chapter_name = %s, chapter_content = %s where id= %s",
                    (item['name'], item['chapter_name'], item['chapter_content'], ids))
            self.connect.commit()
        except Exception as error:
            # print error
            print(error)
        return item

    # TODO 转换text 文件
    # curPath = '全书网小说'
    # tempPath = str(item['name'])
    # targetPath = curPath + os.path.sep + tempPath
    # if not os.path.exists(targetPath):
    #     os.makedirs(targetPath)
    #
    # filename_path = '全书网小说' + os.path.sep + str(item['name']) + os.path.sep + str(
    #     item['chapter_name']) + '.txt'
    # with open(filename_path, 'w', encoding='utf-8') as f:
    #     f.write(item['chapter_content'] + "\n")
