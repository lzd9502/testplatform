import sys
import re

from tester.models import Task as task_model
from tester.serializers import TaskListSerializer
print(__import__)
print(dir(sys.modules[__name__]))
print(sys.modules)
print(sys.modules[__name__])
print(sys.argv)

class Task:
    _id=None
    case=None
    route=None
    data_source=None
    env_config=None
    def __init__(self,task_id):
        self._id=task_id
        task=task_model.objects.get(id=self._id)
        serializer=TaskListSerializer(task)
        _data=serializer.data
