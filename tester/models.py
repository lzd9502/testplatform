from django.db import models
from testenvconfig.models import Project
from django.contrib.auth import get_user_model

user=get_user_model()
# Create your models here.
class route(models.Model):
    '''

    '''
    name = models.CharField(max_length=16, verbose_name='routeName')
    route = models.CharField(max_length=50, verbose_name='route')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='myroute')
    pass


class routeParams(models.Model):
    type_choice = [(0, 'header'), (1, 'param'), (2, 'body'), (3, 'urlparam')]
    param = models.CharField(max_length=16, verbose_name='参数名')
    datatype = models.CharField(choices=type_choice, default=1, verbose_name='参数形式')
    route = models.ForeignKey(route, on_delete=models.CASCADE, verbose_name='所属路由',related_name='myrouteparams')


class routeResponseGroup(models.Model):
    name = models.CharField(max_length=16, verbose_name='responseGroupName')
    route = models.ForeignKey(route, on_delete=models.CASCADE, verbose_name='所属路由',related_name='myresponsegroup')


class ResponseGroupParam(models.Model):
    param = models.CharField(max_length=16, verbose_name='参数名')
    Group = models.ForeignKey(routeResponseGroup, on_delete=models.CASCADE,related_name='mygroupparams')


class case(models.Model):
    name=models.CharField(max_length=16,verbose_name='用例名')
    route=models.ForeignKey(route,on_delete=models.SET_NULL,related_name='mycase')
    createtime=models.DateTimeField(auto_now_add=True)
    createby=models.ForeignKey(user,on_delete=models.SET_NULL)
    updatetime=models.DateTimeField(auto_now=True)
    lastupdateby=models.ForeignKey(user,on_delete=models.SET_NULL)
    pass


class result(models.Model):
    pass
