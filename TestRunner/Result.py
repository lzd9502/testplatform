import sys
import io

# from TestRunner.Parser import Dict

STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'


class BaseResult:
    testsRun=0
    skipped=[]
    errors=[]
    success=[]
    failed=[]
    def __init__(self, stream=None, task=None,buildNumber=None):
        from tester.models import Task as task_model
        self.buildNumber=buildNumber
        self.task=task_model.objects.filter(id=task)[0]
        self.buffer=False
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
    def _add(self,data,test,reason,result_type=None):
        from tester.models import Case
        current_data={}
        current_data['case']=Case.objects.filter(id=test.parser.id)[0]
        current_data['msg']=reason
        current_data['result']=result_type
        current_data['task']=self.task
        current_data['buildNumber']=self.buildNumber
        data.append(current_data)
        pass
    def addskip(self,test,reason):
        self._add(self.skipped, test, reason,'skip')
        # self.skipped.append((test,reason))
    def adderror(self,test,error):
        self._add(self.errors, test, error,'error')
        # self.errors.append((test,error))
    def addfailed(self,test,fail):
        self._add(self.failed, test, fail,'fail')
        # self.failed.append((test,fail))
    def addsuccess(self,test):
        self._add(self.success,test,None,'success')
        pass
    def upload(self):
        from tester.models import Result,Case as case_model
        result_datas=self.success+self.skipped+self.failed+self.errors
        # for x in result_datas:
        #     x['case']=case_model.objects.get(id=x.get('case'))
        result=[Result(**result_data) for result_data in result_datas]
        Result.objects.bulk_create(result)
        pass
    def _setupStdout(self):
        if self.buffer:
            if self._stderr_buffer is None:
                self._stderr_buffer = io.StringIO()
                self._stdout_buffer = io.StringIO()
            sys.stdout = self._stdout_buffer
            sys.stderr = self._stderr_buffer
    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun += 1
        self._mirrorOutput = False
        self._setupStdout()
    def stopTest(self, test):
        """Called when the given test has been run"""
        self._restoreStdout()
        self._mirrorOutput = False

    def _restoreStdout(self):
        if self.buffer:
            if self._mirrorOutput:
                output = sys.stdout.getvalue()
                error = sys.stderr.getvalue()
                if output:
                    if not output.endswith('\n'):
                        output += '\n'
                    self._original_stdout.write(STDOUT_LINE % output)
                if error:
                    if not error.endswith('\n'):
                        error += '\n'
                    self._original_stderr.write(STDERR_LINE % error)

            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._stdout_buffer.seek(0)
            self._stdout_buffer.truncate()
            self._stderr_buffer.seek(0)
            self._stderr_buffer.truncate()
    pass
if __name__ == '__main__':
    import os,django
    curPath = os.path.abspath(os.path.dirname(__file__))
    PathProject = os.path.split(curPath)[0]
    # print(PathProject)
    sys.path.append(PathProject)
    # print(os.environ)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testplatform.settings")
    # print(os.environ)
    django.setup()
    result=BaseResult(task=10)
    result.addsuccess(1)
    result.addsuccess(2)
    result.adderror(1,['wocao','nima'])
    result.addskip(2,'wocao')
    result.upload()
    print(result.skipped,'\n',result.success,'\n',)