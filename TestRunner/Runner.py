import sys

#抄自Unittest.runner,重写write进行自动换行
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
class BaseRunner:
    _result=BaseResult
    def __init__(self,stream=None,result=None,):
        if stream is None:
            stream=sys.stderr
        self.stream=_WritelnDecorator(stream)
        if result:
            self.result=result
    def _initResult(self):
        return self.result(self.stream)
    def run(self,test):
        result=self._initResult()

        pass
