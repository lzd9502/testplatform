import requests
# Create your tests here.
URL="http://127.0.0.1:8000/"
res = requests.post(URL + 'login/', data={'username': 'lzd', 'password': 'lzd19950223'}).json()
headers = {}
headers['Authorization'] = 'MyToken ' + res['token']
JSONHeaders = {}
JSONHeaders['Content-Type'] = 'application/json'
JSONHeaders['Authorization'] = 'MyToken ' + res['token']
#查询全部DataSource
print('查询某项目下全部DataSource:')
AllDataSource=requests.get(URL+'datasource',headers=headers,params={'project':''}).json()
print(AllDataSource)
#插入DataSource
# print('插入DataSource：')
# datas={'name':'apisource','source_type':0,'source_value_runner':'select csf,ewg,safw from api','project':1,'children':[{'name':'csf'},{'name':'ewg'},{'name':'safw'}]}
# SetDataSource=requests.post(URL+'datasource/',headers=headers,json=datas).json()
# print(SetDataSource)