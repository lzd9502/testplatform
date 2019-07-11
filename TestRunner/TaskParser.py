import sys
import re
import os
import django
import requests

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
        while self.myCSRP:
            param = self.myCSRP.popitem()
            route_param = param.get('route_param')
            data_type = route_param.get('data_type')  # {ID:'',routeparam:{datatype:'',...},datasource:{...}}
            type_param = getattr(self, self._param2source[data_type], None)
            type_param[route_param.get('name')] = None
        pass
    def before_run(self):
        pass
    def run(self):
        _method = self._requests()

        pass

    def result(self):
        pass

class DataSource:
    def __new__(cls, *args, **kwargs):
        pass
