import jenkins
import sys
import copy
server=jenkins.Jenkins(url='http://127.0.0.1:8080',username='lzd9502',password='19950223')
#
# job=server.create_job('PythonApiTestJob3',config_xml=jenkins.EMPTY_CONFIG_XML)
# print('job:',job)
job2=server.get_job_info('Example Task')
print(job2)
print(server.get_all_jobs())
# import os
#
# task_data = {
#     'name': 'ApiTestTask',
#     'project': 1,
#     'disabled': True,
#     'env_config': 1,
#     'description': '用于测试本平台task创建流程的正确性',
#     'myCase': [{'case': 1}, {'case': 2}, {'case': 3}]
# }
#
# while task_data:
#     a=task_data.popitem()
#     print(a)
# # task_data.get('name')
# # #
# # # data,project=task_data.pop('name','project')
# # # print(data,project)
# # runtime='aa'
# # assert type(runtime) is str,('wocao')
# # task_data.get('description')
#
# class Single:
#     def __new__(cls):
#         print('create')
#         if not hasattr(cls, '_instance'):
#             cls._instance = super().__new__(cls)
#         return cls._instance
#
#     def __init__(self):
#         print('new')
#         print(self._instance)
#
#
# # a = Single()
# # b = Single()
# # a.test = 'aaa'
# # print('btest', b.test)
# # print(a,b)
#
# class SingleTest:
#     _instance=None
#     def __new__(cls,*args,**kwargs):
#         if cls._instance is None:
#             print('create')
#             cls._instance=super().__new__(cls)
#         return cls._instance
#     def __init__(self):
#         print('init')
#         print(self._instance)
#         # print('myargs',cls.args)
#
# # at=SingleTest(1,2,3)
# bt=SingleTest()
# # at.__dir__()
# list(bt.__dict__)
# print(sys.platform)
# task_data_copy=copy.deepcopy(task_data)
# task_data['name']='wocao'
# print(task_data_copy)
# print(__file__)
# print(os.path.dirname(__file__))
# print(os.path.abspath(__file__))
# print(os.path.abspath(os.path.dirname(__file__)))
# basepath=os.path.basename(os.path.abspath(os.path.dirname(__file__)))
# print(basepath)
# print(type(basepath))
# normalpath=os.path.normpath(basepath)
# print(normalpath)
# __import__(normalpath)
# name=sys.modules[normalpath]
# # __import__('testconfig')
#
# print(name)
# print(dir(name))
# print(sys.modules.keys())
# import unittest
# import JenkinsServer
# testerpath=os.path.dirname(os.path.dirname(__file__))+'/tester'
# print(testerpath)
# sys.path.insert(0,testerpath)
# path=os.path.basename(testerpath)
# print(path)
# __import__(path)
# print(sys.path)
# name2=sys.modules[path]
# print('name2',name2,'%%%',dir(name2))
# print(dir(__file__))
