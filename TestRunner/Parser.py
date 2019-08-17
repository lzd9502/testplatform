import copy
import sys
import os
import django
import requests
import pymssql

# print(__file__)
# print(sys.path)
# print(os.path.dirname(__file__))
# print(os.path.split(os.path.dirname(__file__)))
curPath = os.path.abspath(os.path.dirname(__file__))
PathProject = os.path.split(curPath)[0]
# print(PathProject)
sys.path.append(PathProject)
# print(os.environ)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testplatform.settings")
# print(os.environ)
django.setup()
from tester.models import Task as task_model, Case as case_model, ROUTEPARAMS_TYPE_CHOICE
from tester.serializers import TaskListSerializer, CaseListSerializer
from TestRunner.Exception import FailError, SkipTest


class TaskParser:
    # 在此实例化时完成所有与测试平台数据库的交互
    case=[]

    def __init__(self, id=None):
        task_queryset = task_model.objects.get(id=id)
        task_data = TaskListSerializer(task_queryset).data
        self.name = task_data.get('name')
        from JenkinsServer.JenkinsServer import Jenkins
        jenkins = Jenkins().CreateJenkinsServer()
        self.buildNumber = jenkins.get_job_info(name=self.name)['nextBuildNumber']
        task_case = [case.get('case') for case in task_data.get('myCase')]
        case_queryset = case_model.objects.filter(id__in=task_case)
        case_serializer = [CaseListSerializer(case).data for case in case_queryset]
        self.env_config = task_data.get('env_config')
        # for case_ser in case_serializer:
        #     apicase=ApiParser(case_ser, run_path=self.env_config)
        #     self.case.append(apicase)
        self.case+=case_serializer
    def getCaseData(self):
        return self.case
    def getEnvConfig(self):
        return self.env_config or None


class ApiParser:
    '''
    与数据库交互后的case进行处理
    '''
    req_method = None
    myCSRP = None
    myCSRR = None
    #list,dict等可变对象作为类属性会被共享，变量的初始化应在init中进行

    def __init__(self, case_data=None, run_path=None):
        assert any((case_data, run_path)) is not None, ('Case_data and Case_config must given!')
        self.run_path = run_path
        for k, v in case_data.items():
            self.__setattr__(k, v)
        self._result_data={}
        self._Param_Type_Mapper = {}
        self._ParamParser = []
        self._Response_ParamParser = []
        pass

    def _initParamType(self):
        # todo:当序列化器实现choices时，弃用
        for k in ROUTEPARAMS_TYPE_CHOICE:
            assert type(k[-1]) is str, ('parase route_type error')
            self.__setattr__(k[-1], {})
            self._Param_Type_Mapper[k[0]] = k[-1]
        return self._Param_Type_Mapper

    def _initRequestsData(self):
        assert self.myCSRP is not None, ('error case with None RouteParams!')
        myCSRP = copy.deepcopy(self.myCSRP)
        myCSRR = copy.deepcopy(self.myCSRR)
        while myCSRP:
            csrp = myCSRP.pop()
            route_param = csrp.get('route_param')
            data_type = int(route_param.get('data_type'))  # {ID:'',routeparam:{datatype:'',...},datasource:{...}}
            data_source = csrp.get('data_source')
            param_parser = ParamParser(data_source)
            self._ParamParser.append(param_parser)
            type_param = getattr(self, self._Param_Type_Mapper[data_type],
                                 ValueError('Error Value With %s:%s' % (self, self._Param_Type_Mapper[data_type])))
            type_param[route_param.get('param')] = (param_parser, data_source.get('name'))
        while myCSRR:
            csrr = myCSRR.pop()
            response_param = csrr.get('response').get('param')
            data_source = csrr.get('data_source')
            response_param_parser = ParamParser(data_source, create=False)
            self._Response_ParamParser.append(response_param_parser)
            self._result_data[response_param] = (response_param_parser, data_source['name'])

        pass

    def _initUrl(self):
        host = self.run_path.get('host')
        port = self.run_path.get('port')
        config = ''.join((host, ':', port)) if port else host
        route = self.route.get('route')
        url_params = ''.join([''.join(('/', values)) for values in self.url_param.values()])
        self.URL = ''.join((config, route, url_params)) if route.startswith('/') else ''.join(
            (config, '/', route, url_params))
        pass

    def getConnecttion(self):
        # todo:数据库支持
        from TestRunner.Connect import ConnectFactory
        fact = ConnectFactory()
        # fact.setConnectInfo(dbhost='127,0,0,1', dbport='1433', database='WdEduWisdomSchoolTest', user='select',
        #                       password='select2018')
        return fact

    def getRequestsMethods(self):
        assert 'req_method' in self.__dict__.keys(), ('not inference requests method!')
        return getattr(requests, self.req_method.lower(), None)

    def getResponse(self):
        return self._result_data

    def data_register(self):
        # 数据解析

        dataConnect = self.getConnecttion()
        for dataparser in self._ParamParser:
            dataparser.execute(runner=dataConnect)
        paramList = [getattr(self, value[-1]) for value in ROUTEPARAMS_TYPE_CHOICE]
        for param in paramList:
            for k, v in param.items():
                param[k] = getattr(v[0], v[-1])
        pass

    def response_register(self):
        dataConnect = self.getConnecttion()
        for parser in self._Response_ParamParser:
            parser.execute(runner=dataConnect)
        for k, v in self._result_data.items():
            self._result_data[k] = getattr(v[0], v[-1])

    def register(self):
        init_list = [getattr(self, initter) for initter in self.__dir__() if initter.startswith('_init')]
        for initter in init_list:
            initter()
        # [getattr(self,func,None) for func in function if func is not None]
        # function=[re.match('_init',func) for func in self.__dir__()]

    def __getattr__(self, item):
        return None


class ParamParser:
    # 状态管理模式??解析对象
    _id = {}
    _instance = None
    _creater = None
    _runner = None

    def __new__(cls, instance_data, create=True):
        _instance_data = dict_to_object(instance_data)
        datasource = _instance_data.datasource
        _instance_id = datasource.id
        if cls._id == {} or _instance_id not in cls._id.keys():
            cls._instance = super().__new__(cls)
            cls._id[_instance_id] = cls._instance
        return cls._id[_instance_id]

    def __init__(self, instance_data, create=True):
        _instance_data = dict_to_object(instance_data)
        # self.__setattr__(_instance_data.name, None)
        self._creater = _instance_data.datasource.source_creater
        self._runner = _instance_data.datasource.source_runner
        self._source_type = int(_instance_data.datasource.source_type)
        self._name = _instance_data.datasource.name
        self._UseCreateWhileRunnerResIsNone = create

    def __getattr__(self, item):
        if self._source_type == 1 and self._runner_res:
            return self._runner_res
        else:
            return None

    def execute(self, runner=None):
        # assert isinstance(runner, Connect), TypeError('Error Type of Runner:%s,must a Connect Object', type(runner))
        runner = runner.getConnect(self._source_type)
        runner.connect()
        self._runner_res = runner.execute(self._runner)
        from collections import Iterable
        if not self._runner_res and self._creater:
            if self._UseCreateWhileRunnerResIsNone:
                self._runner_res = runner.execute(self._creater)
            else:
                raise FailError('DataSource Run Result Is None,the runner name:%s' % self._name)
        if not self._runner_res:
            raise SkipTest('init request data err')
        if isinstance(self._runner_res, dict):
            [self.__setattr__(k, self._runner_res[k]) for k in self._runner_res.keys()]
        # elif isinstance(self._runner_res,Iterable):
        #     [self.__setattr__() for k in self._runner_res]

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
    task = TaskParser(10)
    cases = task.case
    [case.register() for case in cases]
    [case.data_register() for case in cases]
