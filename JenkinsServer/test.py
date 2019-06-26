import jenkins

server=jenkins.Jenkins(url='http://127.0.0.1:8080',username='lzd',password='19950223')

# server.create_job('PythonApiTestJob',config_xml=jenkins.EMPTY_CONFIG_XML)

buildinfo=server.get_build_info('the exp test',1)
print('buildinfo:',buildinfo)
print(server.get_all_jobs())