import pymysql as ps
from scrapy.utils.project import get_project_settings


class MysqlHelper:
    def __init__(self):
        self.settings = get_project_settings()  # 获取settings配置数据

        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.password = self.settings['MYSQL_PASSWD']
        self.database = self.settings['MYSQL_DBNAME']
        self.charset = 'utf8'
        self.db = None
        self.curs = None

    # 数据库连接
    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                             charset=self.charset)
        self.curs = self.db.cursor()

    # 数据库关闭
    def close(self):
        self.curs.close()
        self.db.close()

    # 数据增删改
    def cud(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            self.db.commit()
            print("cud ok")
        except:
            print('cud 出现错误')
            self.db.rollback()
        self.close()

    # 数据查询
    def get(self, sql, params):
        self.open()
        try:
            result = self.curs.execute(sql, params)
            self.close()
            print("get ok")
            return result
        except:
            print('get 出现错误')

    # 数据查询
    def find(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            result = self.curs.fetchone()
            self.close()
            print("find ok")
            return result
        except:
            print('find 出现错误')
