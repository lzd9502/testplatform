import sys
import re
import os
import django

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


from tester.models import Task as task_model
from tester.serializers import TaskListSerializer
from testenvconfig.models import ProjectConfig
from testenvconfig.serializers import ProjectConfigSerializer

class Task:
    _id=None
    _data=None
    name=None
    case=None
    route=None
    data_source=None
    env_config=None
    def __init__(self,task_id):
        self._id=task_id
        task=task_model.objects.get(id=self._id)
        serializer=TaskListSerializer(task)
        _data=serializer.data
        self.name=_data.get('name')
    def initCase(self):
        assert self._data.get('myCase') is not None,('注册Case失败,未找到Case!')
        caselist=self._data.get('myCase')
        self.case=[case.get('id') for case in caselist if case.get('disabled')]
        return self.case
    def initConfig(self):
        assert 'env_config' in self._data.keys(),('注册项目运行环境失败，未找到项目环境')
        Config_id=self._data.get('env_config')
        queryset=ProjectConfig.objects.get(id=Config_id)
        return ProjectConfigSerializer(queryset).data
        pass



def initTask(task_id):
    task=task_model.objects.get(id=task_id)
    # case
