import sys
import time

from TestRunner.Case import Case
from TestRunner.Result import BaseResult
from TestRunner.Parser import TaskParser

# 抄自Unittest.runner,重写write进行自动换行
class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""

    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')


class TaskRunner:
    _result = BaseResult
    _tests = []

    def __init__(self, stream=None, result=None, ):
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        if result:
            self._result = result

    def __iter__(self):
        return iter(self._tests)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def Result(self):
        return self._result

    def run(self, task):
        task_data = TaskParser(task)
        result = self.Result()(stream=self.stream, buildNumber=task_data.buildNumber, task=int(task))
        self._tests+=task_data.getCaseData()
        envConfig=task_data.getEnvConfig()
        startTime = time.time()
        for index, case in enumerate(self):
            TestCase=Case(case,envConfig)
            TestCase(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        self.stream.writeln('run %d test in %.2fs' % (result.testsRun, timeTaken))
        self.stream.writeln()
        try:
            # result.upload()
            pass
        except Exception as e:
            self.stream.writeln('result upload err,err msg:')
            self.stream.writeln(str(e.args))
            raise e
        return result
        pass
if __name__ == '__main__':
    task=TaskRunner()
    a=task.run(task=10)
    print('\nsuccess\n',a.success, '\nerror:\n', a.errors, '\nskip:\n', a.skipped,'\nfailed\n',a.failed)