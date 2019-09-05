测试平台（API&WebUI）
=====
进度
-----
目前已逐步完成了API测试相关内容，UI相关开发工作未开始；<br>
<br>
Example
---
项目根路径下Example.py文件以本平台提供的Task的create接口为测试目标，展示了如何通过API调用在项目下完成一个API测试用例并让它自动运行。<br>
<br>
API测试
-----
目前完成了API测试（现仅支持HTTPS协议）相关model设计，接口基本开发完成，核心业务参照了unittest下的case，result,suite等模块进行编写，基本满足了接口测试用例的数据库读写及用例运行、运行结果的写入与存储。
首先回顾单元测试，其测试实现主要分为三部分任务：
* 构造待测逻辑所需的测试数据（入参与期望）；
* 调用被测函数（方法），将构造的测试数据中作为入参的部分传入被测方法；
* 将构造的数据与期望数据进行比较，将测试结论记录输出。<br>
<br>
接口测试同样可用相同的方式对测试任务进行划分。<br>
根据以上理解，在本平台的设计中，将接口测试主体内容分解为三部分：数据源（DataSource）、被测对象（即路由Route Object）、测试结论（Result）。<br>
我们希望DataSource完成任务1，构造测试所需的全部数据；Route是用户自定义的被测接口，开放Header、body、params、Response等可编辑对象；Result完成每轮测试结果与数据库的交互，最终由客户端主动通过平台提供的Api获取生产结果。<br>
同时鉴于多个不同的测试可能需要用到同一个数据源的特性，DataSource设计上完全独立于测试用例.<br>
##DataSource
如下即DataSource的序列化器相关字段信息。runner提供可执行语句，creater是在runner无法正确获取数据时的补充语句（多用于数据库语句，数据库中不一定存在设置条件的数据，creater提供针对Null的处理）
```python
DataSourceSerializer():
    id = IntegerField(label='ID', read_only=True)
    children = SourceResultSerializer(many=True):
        id = IntegerField(label='ID', read_only=True)
        name = CharField(label='结果名', max_length=64)
    name = CharField(label='源名', max_length=64)
    source_type = ChoiceField(choices=((0, 'sql'), (1, 'fix'), (2, 'function')), label='数据源形式', required=False)
    source_runner = CharField(label='源数据获取器', max_length=500, style={'base_template': 'textarea.html'})
    source_creater = CharField(allow_blank=True, allow_null=True, label='源数据生成器', max_length=500, required=False, style={'base_template': 'textarea.html'})
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())
```
由此引申出测试用例（Case）的概念。<br>
##Case
case即单元测试过程中所编写的测试方法。按照单元测试中的经验，它需要存储DataSource与被测方法（Route）可编辑字段多对多的映射关系，以及获取完成接口测试所需的全部信息.<br>
```python
CaseListSerializer():
    id = IntegerField(label='ID', read_only=True)
    route = RouteModelSerializer()
    myCSRP = CSRPListSerializer(many=True)
    myCSRR = CSRRListSerializer(many=True)
    name = CharField(label='用例名', max_length=64)
    req_method = ChoiceField(choices=(('GET', 'get'), ('POST', 'post'), ('PUT', 'put'), ('DELETE', 'delete')), required=False)
    disabled = BooleanField(required=False)
    fixed = ChoiceField(choices=((0, 'error'), (1, 'normal')), required=False)
    createtime = DateTimeField(read_only=True)
    updatetime = DateTimeField(read_only=True)
```
以上是部分Case的序列化器，CSRP为Case-SourceData-RouteParam（入参名与其参数值的映射）的简称，CSRR同理，一个用例根据内部逻辑不同有多个响应体（这在Route处定义），CSRR即本用例选取的响应体期望参数的参数名与其值的映射.<br>
<br>
##Task
Task（自动化测试任务）是Case的集合，Case依赖于Task配置的环境才能执行，用例的执行可以存在于多个Task中.<br>
上文中提到接口测试完成需要更多接口信息，如测试环境（projectConfig），数据库环境（DataSourceConfig），这些内容在Task中给定.你可以配置选取同样的用例，在多个不同的测试环境中执行。<br>
<br>
###TaskModel保存的部分信息
用户写入的Task信息部分保存在数据库中，其他均写入第三方工具Jenkins.<br>
```python
TaskListSerializer():
    id = IntegerField(label='ID', read_only=True)
    myCase = Task2CaseListSerializer(many=True)
    env_config = ProjectConfigSerializer():
        id = IntegerField(label='ID', read_only=True)
        name = CharField(label='配置名称', max_length=20)
        host = IPAddressField(label='服务端地址')
        port = CharField(allow_blank=True, allow_null=True, label='端口号', max_length=10, required=False)
    name = CharField(label='任务名称', max_length=64, validators=[<UniqueValidator(queryset=Task.objects.all())>])
    description = CharField(allow_blank=True, allow_null=True, label='任务简介', max_length=200, required=False, style={'base_template': 'textarea.html'})
    project = PrimaryKeyRelatedField(queryset=Project.objects.all())
```
测试运行-TestRunner
------
TestRunner包内容简单如下：<br>
<br>
* Case：提供APICase运行逻辑与断言逻辑；
* Command：命令模式提供WindowsCMD命令启动测试；
* Connect：提供数据库连接及可用的随机生成数据方法（未实现随机数据包）；
* Exception：必要的异常定义；
* manage：测试主程序执行入口：~/manage.py -runtask --task 4;
* Parser:测试信息数据解析与简单校验；
* Result：实现保存各Case结果与数据库写入；
* Runner：提供Task批量执行Case的方式；