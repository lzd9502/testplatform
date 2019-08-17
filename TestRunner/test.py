import requests
from TestRunner.Parser import ApiParser
from TestRunner.Case import Case
from tester.serializers import CaseListSerializer, TaskListSerializer
from tester.models import Case as case_model, Task as task_model

# -----------------------测试调用API前拿到Token
url = 'http://127.0.0.1:8000'
res = requests.post(url + '/login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
JSONHeaders = {}
JSONHeaders['Content-Type'] = 'application/json'

# case1:正确的Task创建
# case2:重复的Task name属性
# case3:错误的run_time

# 1、给project添加一个Route对象
print('写入route：')
routeDatas = {
    'name': 'Example Route', 'route': '/task',
    'project': 2,
    # datatype:((0, 'header'), (1, 'param'), (2, 'body'), (3, 'url_param'))
    'myrouteparams': [
        {'param': 'name', 'data_type': 2},
        {'param': 'project', 'data_type': 2},
        {'param': 'env_config', 'data_type': 2},
        {'param': 'run_time', 'data_type': 2},
        {'param': 'myCase', 'data_type': 2}, ],
    # todo:response作为一个对象，无法验证cookie，header，statusCode，待优化
    # 三组可能的response的body参数
    'myresponsegroup': [
        {'name': 'SuccessPostGroup', 'mygroupparams': [{'param': 'name'}, {'param': 'project'}]},
        {'name': 'RepeatNameGroup', 'mygroupparams': [{'param': 'Detail'}]},
        {'name': 'ErrJenkinsServerGroup', 'mygroupparams': [{'param': 'Detail'}]}]
}
setroute = requests.post(url + '/route/', headers=headers, json=routeDatas)
if setroute.status_code != 404:
    print(setroute.json())

# 2、创建基于以上创建的Route对象的测试用例，并配置后续用例所需的数据源
# TODO：数据源不够强大，case登陆未处理，function无法配置参数
print('create DataSource for example case：')
#重复的TaskName数据源
RepeatName_datas = {
    'name': 'RepeatTaskNameSource',
    'source_type': 0,
    'source_runner': 'SELECT * FROM tester_task LIMIT 1',
    # TODO：creater输出污染测试库，case 执行后决定是否删除
    'source_creater': 'INSERT INTO tester_task (name,project_id,env_config_id) VALUES ("test creater",1,1);SELECT * FROM tester_task WHERE name=\'test creater\'',
    'project': 2,
    'children': [
        {'name': 'name'},
        {'name': 'project_id'},
        {'name': 'env_config_id'}]}
setRepeatTaskNameResponse = requests.post(url + '/datasource/', headers=headers, json=RepeatName_datas)
if setRepeatTaskNameResponse.status_code != 404:
    print(setRepeatTaskNameResponse.json())
#重复TaskName数据的接口返回结果
theRepeatNameResponse_datas = {
    'name': 'RepeatTaskNameResponse',
    'source_type': 1,
    'source_runner': 'Repeat Task in your project',
    'source_creater': '',
    'project': 2,
    'children': [
        {'name': 'Detail'},]}
setRepeatTaskNameResponseResponse = requests.post(url + '/datasource/', headers=headers, json=theRepeatNameResponse_datas)
if setRepeatTaskNameResponseResponse.status_code != 404:
    print(setRepeatTaskNameResponseResponse.json())
#时间戳表示的绝对不重复的TaskName数据源
AllRightTaskName_datas = {
    'name': 'RightTaskName',
    'source_type': 1,
    'source_runner': 'ExampleRightName+time.time()',
    # TODO：creater输出污染测试库，case 执行后决定是否删除
    'source_creater': '',
    'project': 2,
    'children': [
        {'name': 'name'}, ]}
setAllRightResponse = requests.post(url + '/datasource/', headers=headers, json=AllRightTaskName_datas)
if setAllRightResponse.status_code != 404:
    print(setAllRightResponse.json())
#与测试内容无关的其他必要数据构造1
AllRightTaskProAndConfigAttr_datas = {
    'name': 'RightTaskPro&Config',
    'source_type': 0,
    'source_runner': 'select project_id,id as env_config from testenvconfig_projectconfig limit 1',
    'source_creater': 'insert into testenvconfig_projectconfig(host,port,project_id,name) VALUES (\'127.0.0.1\',\'8080\',1,\'RightTaskTestConfigger\');select project_id,id as env_config from testenvconfig_projectconfig WHERE name=\'RightTaskTestConfigger\'',
    'project': 2,
    'children': [{'name': 'project_id'}, {'name': 'env_config'}]}
setAllRightPCResponse = requests.post(url + '/datasource/', headers=headers, json=AllRightTaskProAndConfigAttr_datas)
if setAllRightPCResponse.status_code != 404:
    print(setAllRightPCResponse.json())
#与测试内容无关的其他必要数据构造2
AllRightTaskOtherAttr_datas = {
    'name': 'AllRightTaskOtherAttr',
    'source_type': 1,
    'source_runner': 'H H * * 1-5',
    'source_creater': '',
    'project': 2,
    'children': [{'name': 'run_time'}]
}
setAllRightOtherResponse = requests.post(url + '/datasource/', headers=headers, json=AllRightTaskOtherAttr_datas)
if setAllRightOtherResponse.status_code != 404:
    print(setAllRightOtherResponse.json())
#创建Task的正确逻辑的返回值数据源，用于
AllRightTaskResponse_datas = {
    'name': 'AllRightTaskResponse',
    'source_type': 0,
    'source_runner': 'select name,project_id from tester_task WHERE name LIKE \'ExampleRightName%\' limit 1',
    'source_creater': '',
    'project': 2,
    'children': [{'name': 'name'}, {'name': 'project_id'}]
}
setAllRightTaskResponse = requests.post(url + '/datasource/', headers=headers, json=AllRightTaskResponse_datas)
if setAllRightTaskResponse.status_code != 404:
    print(setAllRightTaskResponse.json())


def setCSR(route=None, key=None, CSRPDataList=[], CSRRDataList=[]):
    #快速关联方法，将路由中字段名与数据源返回值属性名相同的ID关联，实际可任意组合
    myCSRP = []
    myCSRR = []
    from functools import reduce
    routeParam = route.get('myrouteparams')
    CSRPdatasource = [j.get('children') for j in CSRPDataList]
    CSRPDataSourceList = reduce(lambda x, y: x + y, CSRPdatasource)
    response = [i.get('mygroupparams') for i in route.get('myresponsegroup') if i.get('name') == key]
    for i in routeParam:
        for j in CSRPDataSourceList:
            if i.get('param') == j.get('name'):
                myCSRP.append({'route_param': i.get('id'), 'data_source': j.get('id')})
    try:
        CSRRdatasource = [j.get('children') for j in CSRRDataList]
        CSRRDataSourceList = reduce(lambda x, y: x + y, CSRRdatasource)

        for i in response[-1]:
            for j in CSRRDataSourceList:
                if i.get('param') == j.get('name'):
                    myCSRR.append({'response': i.get('id'), 'data_source': j.get('id')})
    except:
        myCSRR = None
    return myCSRP, myCSRR


# 3、 基于Route对象，创建测试用例，并根据业务逻辑选择不同数据源
print('写入case:')
# 拿到数据源ID
CaseRoute = requests.get(url + '/route', headers=headers, params={'search': 'Example Route'}).json()['results'][-1]
CaseRouteId = CaseRoute.get('id')
PCData = \
    requests.get(url + '/datasource/', headers=headers,
                 params={'search': AllRightTaskProAndConfigAttr_datas.get('name')}).json()['results'][-1]
otherData = requests.get(url + '/datasource/', headers=headers,
                         params={'search': AllRightTaskOtherAttr_datas.get('name')}).json()['results'][-1]
RepeatNameSource = \
    requests.get(url + '/datasource/', headers=headers, params={'search': RepeatName_datas.get('name')}).json()[
        'results'][-1]
RepeatNameResponseSource=requests.get(url + '/datasource/', headers=headers, params={'search': theRepeatNameResponse_datas.get('name')}).json()[
        'results'][-1]
RepeatCSRP, RepeatCSRR = setCSR(route=CaseRoute, key='RepeatNameGroup', CSRPDataList=[RepeatNameSource, otherData],CSRRDataList=[RepeatNameResponseSource,])

AllRightData = \
    requests.get(url + '/datasource/', headers=headers, params={'search': AllRightTaskName_datas.get('name')}).json()[
        'results'][-1]

AllRightResponse = \
requests.get(url + '/datasource/', headers=headers, params={'search': AllRightTaskResponse_datas.get('name')}).json()[
    'results'][-1]
AllRightCSRP, AllRightCSRR = setCSR(route=CaseRoute, key='SuccessPostGroup',
                                    CSRPDataList=[AllRightData, PCData, otherData], CSRRDataList=[AllRightResponse, ])
print(RepeatCSRP,'\n',RepeatCSRR)
print(AllRightCSRP,'\n',AllRightCSRR)
#配置Case，
RepeatCaseData = {'name': 'RepeatTaskNameCase', 'req_method': 'POST', 'route': CaseRouteId, 'project': 2,
                  'myCSRP': RepeatCSRP,
                  'myCSRR': RepeatCSRR}
setrepeatcase = requests.post(url=url + '/case/', headers=headers, json=RepeatCaseData)
if setrepeatcase.status_code != 404:
    print(setrepeatcase.json())
#
AllRightCaseData = {'name': 'AllRightTaskNameCase', 'req_method': 'POST', 'route': CaseRouteId, 'project': 2,
                    'myCSRP': AllRightCSRP,
                    'myCSRR': AllRightCSRR}
setallrightcase = requests.post(url=url + '/case/', headers=headers, json=AllRightCaseData)
if setallrightcase.status_code != 404:
    print(setallrightcase.json())

# 创建Task
#获取到已创建的两个Case
getRepeatCase=requests.get(url+'/case/',headers=headers,params={'search':RepeatCaseData.get('name')}).json()['results'][-1]

getAllRightCase=requests.get(url+'/case/',headers=headers,params={'search':AllRightCaseData.get('name')}).json()['results'][-1]

#post
task_data = {
    'name': 'Example Task',
    'project': 2,
    'env_config': 2,
    'run_time': 'H H * * 1-5',
    'description': 'Task Create Test',
    'myCase': [{'case': getRepeatCase.get('id')}, {'case': getAllRightCase.get('id')}],
}
print('写入task:')
createTask = requests.post(url + '/task/', headers=headers, json=task_data).json()
print(createTask)

findTask=requests.get(url + '/task/10', headers=headers)
print(findTask.json())
