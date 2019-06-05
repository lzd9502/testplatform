from django.test import TestCase
import requests

# Create your tests here.
url = 'http://127.0.0.1:8000/'
res = requests.post(url + 'login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
JSONHeaders = {}
# JSONHeaders['Content-Type'] = 'application/json'
JSONHeaders['Authorization'] = 'MyToken ' + res['token']
# 获取route
print('获取项目下全部route:')
# routeList = requests.get(url + 'route', headers=headers, params={'project': 1}).json()
routeList = requests.get(url + 'route/1', headers=headers).json()
print(routeList)
# 写入route
print('写入route：')
datas = {
    'name': 'TestRouter', 'route': 'xxx/yyy/zzz',
    'project': 1,
    'myrouteparams': [
        {'param': 'apitestparam1', 'datatype': 1},
        {'param': 'apitestparam2', 'datatype': 1}]
    # 'myrouteparams': [
    #     {'aaa': 'apitestparam1', 'datatype': 1},
    #     {'aaa': 'apitestparam2', 'datatype': 1}]
}
setroute = requests.post(url + 'route/', headers=JSONHeaders, data=datas).json()
print(setroute)
