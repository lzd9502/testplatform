import copy
import sys
import re
import os
import django
import requests
import pymssql

print(__file__)
print(sys.path)
print(os.path.dirname(__file__))
print(os.path.split(os.path.dirname(__file__)))
curPath = os.path.abspath(os.path.dirname(__file__))
PathProject = os.path.split(curPath)[0]
print(PathProject)
sys.path.append(PathProject)
print(os.environ)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testplatform.settings")
print(os.environ)
django.setup()

from tester.models import Task2Case as task_model, Case as case_model, ROUTEPARAMS_TYPE_CHOICE
from tester.serializers import TaskListSerializer, CaseListSerializer
from testenvconfig.models import ProjectConfig
from testenvconfig.serializers import ProjectConfigSerializer


class Task:
    _id = None
    _data = None
    name = None
    case = None
    route = None
    data_source = None
    env_config = None

    def __init__(self, task_id):
        self._id = task_id
        task = task_model.objects.get(id=self._id)
        serializer = TaskListSerializer(task)
        _data = serializer.data
        self.name = _data.get('name')

    def initCase(self):
        assert self._data.get('myCase') is not None, ('注册Case失败,未找到Case!')
        case_data = self._data.get('myCase')
        self.case = [case.get('case') for case in case_data]
        case_queryset = case_model.objects.filter(id_in=self.case)
        disabled_map = lambda x: x.disabled
        err_map = lambda x: (not x.disabled) and x.fixed
        disabled_case = map(disabled_map, case_queryset)
        err_case = map(err_map, case_queryset)
        # todo:这里要增加被跳过的用例获取
        return self.case

    def initConfig(self):
        assert 'env_config' in self._data.keys(), ('注册项目运行环境失败，未找到项目环境')
        Config_id = self._data.get('env_config')
        queryset = ProjectConfig.objects.get(id=Config_id)
        return ProjectConfigSerializer(queryset).data
        pass


class Task:
    name = None

    def __new__(cls, id=None, **kwargs):
        assert id is not None, ('注册Task失败!缺少唯一参数值')
        task_queryset = task_model.objects.get(id)
        task_data = TaskListSerializer(task_queryset).data
        cls.name = task_data.get('name')
        task_case = [case.get('case') for case in task_data.get('myCase')]
        case_queryset = case_model.objects.filter(id__in=task_case)
        disabled_map = lambda x: x.disabled
        err_map = lambda x: (not x.disabled) and x.fixed
        disabled_case = map(disabled_map, case_queryset)
        err_case = map(err_map, case_queryset)
        case = CaseListSerializer(case_queryset)
        return super().__new__(cls)

    def run(self):
        pass


class Case:
    req_method = None
    myCSRP = None
    myCSRR = None
    _result = None
    _param2source = {}

    def __new__(cls, case):
        for k, v in case:
            cls.__setattr__(k, v)
        for k in ROUTEPARAMS_TYPE_CHOICE:
            assert type(k[-1]) is str, ('parase route_type error')
            cls.__setattr__(k[-1], {})
            cls._param2source[k[0]] = k[-1]
        return super().__new__(cls)
        pass

    def _requests(self):
        assert '_req_method' in self.__dict__, ('not inference requests method!')
        return getattr(requests, self.req_method.lower())

    def initRequests(self):
        assert 'myCSRP' in self.__dict__, ('error case with None RouteParams!')
        myCSRP = copy.deepcopy(self.myCSRP)
        data_source = []
        while myCSRP:
            csrp = myCSRP.popitem()
            route_param = csrp.get('route_param')
            data_type = route_param.get('data_type')  # {ID:'',routeparam:{datatype:'',...},datasource:{...}}
            source_data = csrp.get('data_source').get
            type_param = getattr(self, self._param2source[data_type], None)
            type_param[route_param.get('name')] = None
        pass

    def _initDataSourceConfig(self):
        # todo:此处应根据用户项目设置的数据库类型返回对应实例
        return DataSource('192.168.3.251', '1433', 'WdEduWisdomSchoolTest', 'select', 'select2018').create()

    def initDataSource(self):

        pass

    def before_run(self):
        pass

    def run(self):
        _method = self._requests()

        pass

    def result(self):
        pass


class ParamParaser:
    # 状态管理模式??
    _id = {}
    _instance = None
    creater = None
    runner = None

    def __new__(cls, instance_data):
        _instance_data = dict_to_object(instance_data)
        datasource = _instance_data.datasource
        _instance_id = datasource.id
        print('_id:',cls._id)
        if cls._id =={} or _instance_id not in cls._id.keys():

            cls._instance = super().__new__(cls)
            cls._id[_instance_id]=cls._instance
        # cls.__setattr__[_instance_data.name]=None
        return cls._id[_instance_id]

    def __init__(self, instance_data):
        _instance_data = dict_to_object(instance_data)
        self.__setattr__(_instance_data.name, None)
        self.creater = _instance_data.datasource.source_creater
        self.runner = _instance_data.datasource.source_runner


class DataSource:
    data = None

    def __init__(self, dbhost=None, dbport=None, database=None, user=None, password=None, isdict=True):
        self.server = dbhost + dbport
        self.database = database
        self.user = user
        self.password = password
        self.isdict = isdict

    def excute(self, script):
        cursor = self.ss.cursor()
        cursor.execute(script)
        res = cursor.fetchone()
        cursor.close()
        return res

    def _create(self):
        try:
            self.ss = pymssql.connect(server=self.server, user=self.user, password=self.password,
                                      database=self.database,
                                      as_dict=self.isdict)
        except pymssql.OperationalError:
            self.ss = None
            raise ConnectionError('连接数据库失败')
        return self.ss


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst


if __name__ == '__main__':
    from tester.serializers import CaseListSerializer
    from tester.models import Case
    import copy

    que = Case.objects.get(id=2)
    ser = CaseListSerializer(que).data
    a_dict = ser.get('myCSRP')[0].get('data_source')
    b_dict = copy.deepcopy(a_dict)
    b_dict.get('datasource')['id'] = 2
    ap = ParamParaser(a_dict)
    bp = ParamParaser(b_dict)
    cp = ParamParaser(a_dict)
    ap.runner = 1
    bp.runner=2
    ap.csf='csf'
    bp.csf
    print(ap.runner,bp.runner, cp.runner)
    print(ap.csf,bp.csf,cp.csf)
