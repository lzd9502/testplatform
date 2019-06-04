from django.test import TestCase
import requests

# Create your tests here.
url = 'http://127.0.0.1:8000/'
res = requests.post(url + 'login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
# 获取route
print('获取项目下全部route:')
routeList = requests.get(url + 'route', headers=headers, params={'project':1}).json()
# routeList = requests.get(url + 'route', headers=headers).json()
print(routeList)
# 写入route
# print('写入route：')
# setroute = requests.post(url + 'route/', headers=headers, data={'name': 'TestRouter', 'route': 'xxx/yyy/zzz','project': 1,
#                                                                 'myrouteparams': [
#                                                                     {'param': 'apitestparam1', 'datatype': 0},
#                                                                     {'param': 'apitestparam2', 'datatype': 1}]
#                                                                 }).json()
# print(setroute)
