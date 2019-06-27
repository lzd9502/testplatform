from django.test import TestCase
import requests

# Create your tests here.
url = 'http://127.0.0.1:8000/'
res = requests.post(url + 'login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
JSONHeaders = {}
JSONHeaders['Content-Type'] = 'application/json'
JSONHeaders['Authorization'] = 'MyToken ' + res['token']
# 获取route
# print('获取项目下全部route:')
# routeList = requests.get(url + 'route', headers=headers,
#                          params={'project': 1, 'search': '', 'page_size': 20, 'page': 1}).json()
# routeList = requests.get(url + 'route/', headers=headers).json()
# print(routeList)
# 写入route
# print('写入route：')
# datas = {
#     'name': 'TestGroup3', 'route': 'xxx/yyy/zzz',
#     'project': 2,
#     'myrouteparams': [
#         {'param': 'apitestparam1', 'datatype': 1},
#         {'param': 'apitestparam2', 'datatype': 1}],
#     'myresponsegroup': [
#         {'name': 'firstgroup',  'mygroupparams': [{'param': '1group1param'}, {'param': '1group2param'}]},
#         {'name': 'firstgroup', 'mygroupparams': [{'param': '1group1param'}, {'param': '1group2param'}]}, ]
#     # 'myresponsegroup': [{'name': 'firstgroup'},{'name':'secondgroup'}],
# }
# setroute = requests.post(url + 'route/', headers=JSONHeaders, json=datas).json()
# print(setroute)

# 查询Case
# print('查询Case:')
# pcase = requests.get(url=url + 'case', headers=headers, params={'project': 1, 'search': 'apicase1'}).json()
# print(pcase)
# 写入case
# print('写入case:')
# casedata={'name':'apicase1','req_method':'POST','project':1,'myCSRP':[{'route_param':1,'data_source':1}],'myCSRR':[{'response':1,'data_source':1}]}
# setcase=requests.post(url=url+'case/',headers=JSONHeaders,json=casedata).json()
# print(setcase)


# 查询task
print('查询task:')
ptask = requests.get(url + 'task', headers=headers, params={'project': 1}).json()
print(ptask)
# 写入task
task_data = {
    'name': 'ApiTestTask',
    'project': 1,
    'disabled': True,
    'env_config': 1,
    'description': '用于测试本平台task创建流程的正确性',
    'myCase': [{'case': 1}, {'case': 2}],
}
# task_data = {
#     'name': 'ApiTestTask',
#     'project': 1,
#     'disabled': True,
#     'env_config': 1,
#     'description': '用于测试本平台task创建流程的正确性',
#     # 'run_'
#     # 'myCase':'',
# }
print('写入task:')
createTask = requests.post(url + 'task/', headers=JSONHeaders, json=task_data).json()
print(createTask)

# sql注入相关
# URL='http://www.zszywx.com/CMSInfo/WebFile/Web_2/html/news_list.html'
# URL2='http://192.168.60.114:6005/CMSInfo/WebFile/Web_2/html/news_list.html'
# data='一张卷'
# #查询失效字符串
# sqldata='一张卷\' or \'1\'=\'1\' or \'1\' !=\''
# sql2data="; and 1=1 and 1=2"
# droptabledata='一张卷\';Drop Table '
# res=requests.get(url=URL,params={'Search':sql2data})
# print(res.text)
