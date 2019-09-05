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
