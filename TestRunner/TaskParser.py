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
        # disabled_map = lambda x: x.disabled
        # err_map = lambda x: (not x.disabled) and x.fixed
        # disabled_case = map(disabled_map, case_queryset)
        # err_case = map(err_map, case_queryset)
        # todo:这里要增加被跳过的用例获取
        return self.case

    def initConfig(self):
        assert 'env_config' in self._data.keys(), ('注册项目运行环境失败，未找到项目环境')
        Config_id = self._data.get('env_config')
        queryset = ProjectConfig.objects.get(id=Config_id)
        return ProjectConfigSerializer(queryset).data
        pass


class TaskParser:
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
        case_serializer = CaseListSerializer(case_queryset)
        return super().__new__(cls)
    # def __init__(self,id=None,**kwargs):

class CaseParser:
    '''
    与数据库交互后的case进行处理
    '''
    req_method = None
    myCSRP = None
    myCSRR = None
    _result = None
    _Param_Type_Mapper = {}

    def __init__(self, case):
        for k, v in case:
            self.__setattr__(k, v)
        self._initParamType()
        pass

    def _initParamType(self):
        # todo:当序列化器实现choices时，弃用
        for k in ROUTEPARAMS_TYPE_CHOICE:
            assert type(k[-1]) is str, ('parase route_type error')
            assert getattr(self, k[-1], None) is not None, ('初始化参数类型错误，与Case对象属性冲突的属性名：%s' % k[-1])
            self.__setattr__(k[-1], {})
            self._Param_Type_Mapper[k[0]] = k[-1]
        return self._Param_Type_Mapper

    def _initRequestsMethods(self):
        assert '_req_method' in self.__dict__.keys(), ('not inference requests method!')
        return getattr(requests, self.req_method.lower())

    def _initRequestsData(self):
        assert self.myCSRP is not None, ('error case with None RouteParams!')
        myCSRP = copy.deepcopy(self.myCSRP)
        while myCSRP:
            csrp = myCSRP.popitem()
            route_param = csrp.get('route_param')
            data_type = route_param.get('data_type')  # {ID:'',routeparam:{datatype:'',...},datasource:{...}}
            data_source = csrp.get('data_source')
            param_parser = ParamParser(data_source)
            type_param = getattr(self, self._Param_Type_Mapper[data_type],
                                 ValueError('Error Value With %s:%s' % (self, self._Param_Type_Mapper[data_type])))
            type_param[route_param.get('name')] = getattr(param_parser, data_source.get('name'))
        pass

    def _initDataSourceConfig(self):
        # todo:此处应根据用户项目设置的数据库类型返回对应实例
        from TestRunner.Connect import DBConnect
        return DBConnect('192.168.3.251', '1433', 'WdEduWisdomSchoolTest', 'select', 'select2018')

    def initDataSource(self):

        pass

    def before_run(self):
        pass

    def run(self,result=None):
        self.before_run()
        _method = self._requests()

        pass



class ParamParser:
    # 状态管理模式??解析对象
    _id = {}
    _instance = None
    _creater = None
    _runner = None

    def __new__(cls, instance_data):
        _instance_data = dict_to_object(instance_data)
        datasource = _instance_data.datasource
        _instance_id = datasource.id
        if cls._id == {} or _instance_id not in cls._id.keys():
            cls._instance = super().__new__(cls)
            cls._id[_instance_id] = cls._instance
        # cls.__setattr__[_instance_data.name]=None
        return cls._id[_instance_id]

    def __init__(self, instance_data):
        _instance_data = dict_to_object(instance_data)
        self.__setattr__(_instance_data.name, None)
        self._creater = _instance_data.datasource.source_creater
        self._runner = _instance_data.datasource.source_runner

    def __getattr__(self, item):
        return None

    def _run(self, runner=None, script=None):
        assert any((runner, script)), ValueError(
            'empty objects or scripts! runner like %s with script like %s' % (runner, script))
        from TestRunner.Connect import Connect
        assert isinstance(runner,Connect),TypeError('Error Type of Runner:%s,must a Connect Object',type(runner))
        self._runner_res = runner.execute(script)
        [self.__setattr__(k,self._runner_res[k]) for k in (self._runner_res.keys() and self.__dict__.keys())]
        pass



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
    print('ser:', ser)
    a_dict = ser.get('myCSRP')[0].get('data_source')
    b_dict = copy.deepcopy(a_dict)
    b_dict.get('datasource')['id'] = 2
    # ap = ParamParser(a_dict)
    # bp = ParamParser(b_dict)
    # cp = ParamParser(a_dict)
    # ap._runner = 1
    # bp._runner = 2
    # ap.csf = 'csf'
    # print(ap._runner, bp._runner, cp._runner)
    # print(ap.csf, bp.csf, cp.csf, bp.ccs, bp.run)
    # print(getattr(ap, 'runner', None))
    # print(ap.__dict__)
    # print('-----------------------------------')
    class a(ParamParser):
        def _run(self, runner=None, script=None):
            self.csf='gaiwanle'
    app=a(a_dict)
    # print(app.csf)
    # app._run()
    # print(app.csf)
    #-------------------------------------------
    print(isinstance(app,a))
    print(isinstance(app,ParamParser))
    print(issubclass(a,ParamParser))
