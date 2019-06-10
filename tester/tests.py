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
print('获取项目下全部route:')
routeList = requests.get(url + 'route', headers=headers,
                         params={'project': 1, 'search': '', 'page_size': 20, 'page': 1}).json()
# routeList = requests.get(url + 'route/', headers=headers).json()
print(routeList)
# 写入route
print('写入route：')
datas = {
    'name': 'TestRouterWGroup', 'route': 'xxx/yyy/zzz',
    'project': 1,
    'myrouteparams': [
        {'param': 'apitestparam1', 'datatype': 1},
        {'param': 'apitestparam2', 'datatype': 1}],
    'myresponsegroup': [{'name': 'firstgroup', 'mygroupparams': [{'param': '1group1param'}, {'param': '1group2param'}]},]
}
setroute = requests.post(url + 'route/', headers=JSONHeaders, json=datas).json()
print(setroute)

# sql注入相关
# URL='http://www.zszywx.com/CMSInfo/WebFile/Web_2/html/news_list.html'
# data='一张卷'
# #查询失效字符串
# sqldata='一张卷\' or \'1\'=\'1\' or \'1\' !=\''
# sql2data="; and 1=1 and 1=2"
# droptabledata='一张卷\';Drop Table '
# res=requests.get(url=URL,params={'Search':sqldata})
# print(res.text)
