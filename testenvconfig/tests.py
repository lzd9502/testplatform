from django.test import TestCase

# Create your tests here.

import requests

url = 'http://127.0.0.1:8000/'
res = requests.post(url + 'login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
#查询个人信息
# print('查询个人信息：')
# userinfo=requests.get(url+'user/info',headers=headers).json()
# print(userinfo)
# 查询用户关联的项目
userproject = requests.get(url + 'user/project', headers=headers).json()
print(userproject)
# 加入项目
# project_id=3
# print('加入项目:',project_id)
# userpost=requests.post(url+'user/project/',headers=headers,data={'Project':project_id}).json()
# print(userpost)
# 创建项目
# CreateProjectName='TestProjectToApiApi'
# print('创建项目:',CreateProjectName)
# CreateUserProject=requests.post(url+'project/',headers=headers,data={'name':CreateProjectName})
# print(CreateUserProject)
# 更改项目
# print('更改项目:')
# PutUserProject = requests.put(url + 'project/2/', headers=headers, data={'name':'TrueTestProject','disabled': True}).json()
# print(PutUserProject)
# 查询项目
# print('查询项目:')
# GetUserProject = requests.get(url + 'project/2/', headers=headers, ).json()
# print(GetUserProject)
