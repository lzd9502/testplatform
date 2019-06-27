import jenkins

# server=jenkins.Jenkins(url='http://127.0.0.1:8080',username='lzd',password='19950223')
#
# # job=server.create_job('PythonApiTestJob2',config_xml=jenkins.EMPTY_CONFIG_XML)
# # print('job:',job)
# job2=server.get_job_info('PythonApiTestJob')
# print(job2)
# buildinfo=server.get_build_info('the exp test',1)
# print('buildinfo:',buildinfo)
# print(server.get_all_jobs())

task_data = {
    'name': 'ApiTestTask',
    'project': 1,
    'disabled': True,
    'env_config': 1,
    'description': '用于测试本平台task创建流程的正确性',
    'myCase': [{'case':1}, {'case':2}, {'case':3}]
}
# #
# # data,project=task_data.pop('name','project')
# # print(data,project)
# runtime=ValueError
# assert type(runtime) is str,('wocao')
print(task_data.get('description'))