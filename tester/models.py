from django.db import models
from testenvconfig.models import Project, ProjectConfig
from dataconfigurator.models import SourceResult
from django.contrib.auth import get_user_model

user = get_user_model()


# Create your models here.

# =====================================================================
# --------------------------------Route--------------------------------
# =====================================================================

class Route(models.Model):
    '''
    路由的基础表
    '''
    name = models.CharField(max_length=16, verbose_name='routeName')
    route = models.CharField(max_length=50, verbose_name='route')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='myroute')
    pass


class RouteParams(models.Model):
    '''
    路由参数表
    '''
    type_choice = ((0, 'header'), (1, 'param'), (2, 'body'), (3, 'url_param'))
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='所属路由', related_name='myrouteparams')
    param = models.CharField(max_length=16, verbose_name='参数名')
    data_type = models.CharField(max_length=1, choices=type_choice, default=1, verbose_name='参数形式')


class RouteResponseGroup(models.Model):
    '''
    路由响应参数组----响应与路由的映射关系表
    '''
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='所属路由', related_name='myresponsegroup')
    name = models.CharField(max_length=16, verbose_name='responseGroupName')


class ResponseGroupParam(models.Model):
    '''
    路由响应参数组----参数与响应的映射关系表
    '''
    Group = models.ForeignKey(RouteResponseGroup, on_delete=models.CASCADE, related_name='mygroupparams')
    param = models.CharField(max_length=16, verbose_name='参数名')


# =====================================================================
# --------------------------------Case---------------------------------
# =====================================================================

class Case(models.Model):
    '''
    用例信息表
    '''
    case_method_choice = (('GET', 'get'), ('POST', 'post'), ('PUT', 'put'), ('DELETE', 'delete'))
    name = models.CharField(max_length=16, verbose_name='用例名')
    req_method = models.CharField(max_length=6, choices=case_method_choice, default=case_method_choice[0])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='mycase')
    createtime = models.DateTimeField(auto_now_add=True)
    createby = models.ForeignKey(user, null=True, on_delete=models.SET_NULL, related_name='casecreater')
    updatetime = models.DateTimeField(auto_now=True)
    updateby = models.ForeignKey(user, null=True, on_delete=models.SET_NULL, related_name='caseupdater')
    pass


class Case_Source_RouteParam(models.Model):
    '''
    用例-数据源-请求参数三方映射表
    '''
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='myCSRP')
    route_param = models.ForeignKey(RouteParams, null=True, on_delete=models.SET_NULL)
    data_source = models.ForeignKey(SourceResult, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('case', 'route_param', 'data_source')


class Case_Source_RouteResponse(models.Model):
    '''
    用例-数据源-响应参数表
    '''
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='myCSRR')
    response = models.ForeignKey(ResponseGroupParam, null=True, on_delete=models.SET_NULL)
    data_source = models.ForeignKey(SourceResult, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('case', 'response', 'data_source')


# class result(models.Model):
#     pass

# ================================================================
# -------------------------------Task-----------------------------
# ================================================================

class Task(models.Model):
    '''
    测试任务表
    '''
    name = models.CharField(max_length=16, verbose_name='任务名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='myTask', )
    env_config = models.ForeignKey(ProjectConfig, null=True,on_delete=models.SET_NULL, related_name='myTask')
    jenkins_job=models.CharField(max_length=32,null=True,blank=True,verbose_name='jenkins任务ID')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='任务简介')


class Task2Case(models.Model):
    '''
    任务-用例映射表
    '''
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='myCase')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='myTask')
    disabled=models.BooleanField(default=True,verbose_name='启用状态')
    create_time=models.DateTimeField(auto_now_add=True)
    create_by=models.ForeignKey(user,null=True,on_delete=models.SET_NULL,related_name='TaskCreatedSelf')
    update_time=models.DateTimeField(auto_now=True,)
    update_by=models.ForeignKey(user,null=True,on_delete=models.SET_NULL,related_name='TaskIUpdatedSelf')

#todo:任务执行流水表