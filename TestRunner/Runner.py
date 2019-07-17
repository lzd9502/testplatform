import sys

#抄自Unittest.runner,重写write进行自动换行
import time
from TestRunner.Result import BaseResult
from TestRunner.TaskParser import TaskParser


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream,attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')
class TaskRunner:
    _result=BaseResult
    _tests=[]
    def __init__(self,stream=None,result=None,):
        if stream is None:
            stream=sys.stderr
        self.stream=_WritelnDecorator(stream)
        if result:
            self.result=result
    def __iter__(self):
        return iter(self._tests)
    def __call__(self, *args, **kwargs):
        return self.run(*args,**kwargs)
    def _initResult(self):
        return self.result(self.stream)
    def run(self,task):
        result=self._initResult()
        task=TaskParser(task)
        self._tests.append(task.case)
        startTime=time.time()
        for index,case in enumerate(self):
            case(result)
        stopTime=time.time()
        timeTaken=stopTime-startTime
        self.stream.writeln('run %d test in %.2fs'%(result.testsRun,timeTaken))
        self.stream.writeln()
        return result
        pass
