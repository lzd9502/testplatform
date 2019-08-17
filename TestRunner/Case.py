import contextlib
import sys

from TestRunner.Parser import ApiParser, SkipTest
from TestRunner.Result import BaseResult
from TestRunner.Exception import FailError, CaseRunError


def compareDict(realResponseDict: dict, preSetDict: dict):
    valueNotEqual = {}
    valueNotCompare = {}
    valueUnset = []
    for i in preSetDict.keys():
        realkey = realResponseDict.keys()
        realValue = None
        if not realkey:
            valueUnset += list(preSetDict.keys())[i + 1:]
            break
        for j in realkey:
            if str(i).lower() == str(j).lower():
                realValue = realResponseDict.pop(j)
                if preSetDict[i] != realValue:
                    valueNotEqual[i] = [preSetDict[i], realValue]
                break
            continue
        if realValue == None:
            valueNotCompare[i] = preSetDict.get(i)
    valueUnset += realResponseDict.keys()
    return valueNotEqual, valueNotCompare, valueUnset


# 抄自unittest，定义了上下文管理器捕获with语句中的异常并执行额外逻辑
class _Outcome(object):
    def __init__(self, result=None):
        self.result = result
        self.success = True
        self.skipped = []
        self.errors = []
        self.failed = []

    @contextlib.contextmanager
    def testPartExecutor(self, test_case):
        old_success = self.success
        self.success = True
        try:
            yield
        except SkipTest as e:
            self.success = False
            self.skipped.append((test_case, str(e)))
        except FailError as e:
            self.success = False
            self.failed.append((test_case, str(e)))
        except:
            exc_info = sys.exc_info()
            self.success = False
            self.errors.append((test_case, exc_info))
            # explicitly break a reference cycle:
            # exc_info -> frame -> exc_info
            exc_info = None
        else:
            pass
        finally:
            self.success = self.success and old_success


class Case:
    parser = None

    def __init__(self, data=None, runPath=None):
        if data is None:
            raise CaseRunError('with out case data run')
        self.parser = ApiParser(data, runPath)
        pass

    def check_status(self):
        if self.parser.disabled:
            raise SkipTest('Case is disabled')
        if not self.parser.fixed:
            raise SkipTest(
                'Case last run failed with some problem not fixed,Please check "fix it" to restart this Case')
        pass

    def before_run(self):
        self.check_status()
        assert self.parser.req_method is not None, ValueError('register request method error')
        self.testMethod = self.parser.getRequestsMethods()
        self.parser.register()
        self.parser.data_register()

    def compareDict(self, realResponseDict: dict, preSetDict: dict):
        valueNotEqual = {}
        valueNotCompare = {}
        valueUnset = []
        popkey = []
        for i in preSetDict.keys():
            realkey = realResponseDict.keys()
            realValue = None
            if not realkey:
                valueUnset += list(preSetDict.keys())[i + 1:]
                break
            for j in realkey:
                if str(i).lower() == str(j).lower():
                    realValue = realResponseDict.pop(j)
                    popkey.append(realValue)
                    if preSetDict[i] != realValue:
                        valueNotEqual[i] = [preSetDict[i], realValue]
                    break
                continue
            if realValue == None:
                valueNotCompare[i] = preSetDict.get(i)
        if popkey == None:
            raise FailError("the datasource set can not compare any response attrbute")
        valueUnset += realResponseDict.keys()
        return valueNotEqual, valueNotCompare, valueUnset

    def result_assert(self, response):
        self.parser.response_register()
        valid_data = self.parser.getResponse()
        err_msg = []
        try:
            NotEqual, NotCompare, UnsetAttr = self.compareDict(response, valid_data)
            if NotEqual:
                for k, v in NotEqual.items():
                    err_msg.append(
                        '\nassert attribute %s failure.\nPreSet Value:\n "%s" \nThe Response value:\n"%s"\nNot Equal' % (
                            k, v[0], v[1]))
            if NotCompare:
                for k, v in NotCompare.items():
                    print('got attr: [%s] value: %s from DataSource u Set but not found in the Case Response' % (k, v),
                          '\n')
            if UnsetAttr:
                print('find attr %s in Case Response, u can set them by datasource' % UnsetAttr, '\n')
        except FailError as e:
            err_msg.append(e)
        except:
            info = sys.exc_info()
            raise CaseRunError(self.parser.name, info)
        finally:
            if err_msg:
                raise FailError(err_msg)
        pass

    def run(self, result=None):
        if result is None:
            result = BaseResult()
        result.startTest(self)
        _outCome = _Outcome(result)
        try:
            with _outCome.testPartExecutor(self):
                self.before_run()
            with _outCome.testPartExecutor(self):
                response = self.testMethod(url=self.parser.URL, params=self.parser.param,
                                           json=self.parser.body, headers=self.parser.header, ).json()
            with _outCome.testPartExecutor(self):
                self.result_assert(response)
            # self.result_assert(response)
            for test, reason in _outCome.skipped:
                result.addskip(test, reason)
            for test, error in _outCome.errors:
                result.adderror(test, error)
            for test, fail in _outCome.failed:
                result.addfailed(test, fail)
            if _outCome.success:
                result.addsuccess(self)
        finally:
            result.stopTest(self)
        return result

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


if __name__ == '__main__':
    a = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    b = {'b': 1, 'c': 3, 'd': 4, 'e': 5}
    z, x, c = compareDict(a, b)
    print(z, '\n', x, '\n', c)
