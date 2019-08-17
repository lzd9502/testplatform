import inspect
import os,sys,pymssql
#todo:这里需要：单例模式的SQL连接+数据库连接池（DBUtils），配合以后可能的多线程用例执行

class Connect:
    #todo:解决Connect基类，处理DataSource_type,根据type提供不同的excute方法,返回dict对象

    def execute(self,script):
        return script
    def connect(self,**kwargs):
        return self
    pass

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
class MockConnect(Connect):
    type=0
    hasconnect=False
    def execute(self,script):
        if not self.hasconnect:
            raise ConnectionError('SQL not connected,run connect() method before execute')
        cur=self.connect.cursor()
        cur.execute(script)
        res=cur.fetchone()
        return res
    def connect(self,path=None):
        import sqlite3
        if path:
            spath=path
        else:
            base = os.path.dirname(os.path.dirname(__file__))
            spath=base + '\db.sqlite3'
        self.connect = sqlite3.connect(spath)
        self.connect.row_factory=dict_factory
        self.hasconnect=True
        return self



class FixConnect(Connect):
    #todo:待改进
    type=1
    def execute(self,script):
        if isinstance(script,int):
            return script
        if isinstance(script,str):
            try:
                script_runner=script.split('+')
                result_values=''
                for runner in script_runner:
                    parse=runner.split('.')
                    if len(parse)>1:
                        is_call = parse[1].split('(')
                        function=getattr(__import__(parse[0]),is_call[0])
                        result=function() if len(is_call)>1 else function
                    elif len(parse[0].split('('))>1:
                        result=getattr(self,parse[0])()
                    else:
                        result=parse[0]
                    result_values+=str(result)
                return result_values
            except:
                return None


    pass

class DBConnect(Connect):

    def execute(self, script):
        cursor = self.ss.cursor()
        cursor.execute(script)
        res = cursor.fetchone()
        cursor.close()
        return res

    def connect(self,dbhost=None, dbport=None, database=None, user=None, password=None,):
        self.server = ''.join((dbhost, ':', dbport)) if not dbhost.endswith(':') or not dbport.startswith(
            ':') else dbhost + dbport
        self.database = database
        self.user = user
        self.password = password
        self.isdict = True
        try:
            self.ss = pymssql.connect(server=self.server, user=self.user, password=self.password,
                                      database=self.database,
                                      as_dict=self.isdict)
        except:
            raise ConnectionError('连接数据库失败')
        return self

CONNECTTYPE={0: MockConnect, 1: FixConnect, 2: Connect}

class ConnectFactory:
    ConnectInfo={}
    def setConnectInfo(self,**kwargs):
        self.ConnectInfo=kwargs
    def getConnect(self,connectType=None):
        # if connectType in CONNECTTYPE:
        #     return CONNECTTYPE[connectType]()
        # else:
        #     return
        connect=[]
        path=dir(sys.modules[__name__])
        res=None
        for i in path:
            type=getattr(sys.modules[__name__],i)
            if not inspect.isclass(type):
                continue
            elif issubclass(type,Connect):
                connect.append(type)
            else:
                continue
        for j in connect:
            if hasattr(j,'type') and connectType==getattr(j,'type',None):
                res=j()
                break
        return res
if __name__ == '__main__':
    # db=DBConnect()
    # db.connect(dbhost='127.0.0.1',dbport='1433',database='testdb',user='sa',password='19950223')
    # res=db.execute('select * from dbo.test1table')
    # print(res)
    a=ConnectFactory()
    z=a.getConnect(0)
    z.connect()
    res=z.execute('select name,project_id from tester_task WHERE name LIKE \'ExampleRightName%\' limit 1')
    print(res)
    # y=a.getConnect(1)
    # y.connect()
    # res=y.execute('ExampleRightName+time.time()')
    # print(res,'\n',len(res))