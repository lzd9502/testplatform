import pymssql
class Connect:
    #todo:解决Connect基类，处理DataSource_type,根据type提供不同的excute方法,返回dict对象

    def execute(self,script):
        return script
    def connect(self):
        raise ConnectionError('Base Connect Object Has No Connect Function')
    pass

class DBConnect(Connect):

    def __init__(self, dbhost=None, dbport=None, database=None, user=None, password=None, isdict=True):
        self.server = dbhost + dbport
        self.database = database
        self.user = user
        self.password = password
        self.isdict = isdict

    def execute(self, script):
        cursor = self.ss.cursor()
        cursor.execute(script)
        res = cursor.fetchone()
        cursor.close()
        return res

    def connect(self):
        try:
            self.ss = pymssql.connect(server=self.server, user=self.user, password=self.password,
                                      database=self.database,
                                      as_dict=self.isdict)
        except pymssql.OperationalError:
            self.ss = None
            raise ConnectionError('连接数据库失败')
        return self.ss
