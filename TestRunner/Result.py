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
    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun += 1
    pass