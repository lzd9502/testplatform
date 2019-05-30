from django.db import models
from testenvconfig.models import Project
from dataconfigurator.models import SourceResult
from django.contrib.auth import get_user_model

user = get_user_model()


# Create your models here.
class Route(models.Model):
    '''

    '''
    name = models.CharField(max_length=16, verbose_name='routeName')
    route = models.CharField(max_length=50, verbose_name='route')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='myroute')
    pass


class RouteParams(models.Model):
    type_choice = [(0, 'header'), (1, 'param'), (2, 'body'), (3, 'url_param')]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='所属路由', related_name='myrouteparams')
    param = models.CharField(max_length=16, verbose_name='参数名')
    datatype = models.CharField(max_length=1, choices=type_choice, default=1, verbose_name='参数形式')


class RouteResponseGroup(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='所属路由', related_name='myresponsegroup')
    name = models.CharField(max_length=16, verbose_name='responseGroupName')


class ResponseGroupParam(models.Model):
    Group = models.ForeignKey(RouteResponseGroup, on_delete=models.CASCADE, related_name='mygroupparams')
    param = models.CharField(max_length=16, verbose_name='参数名')


class Case(models.Model):
    case_method_choice = [('GET','get'), ('POST','post'), ('PUT','put'), ('DELETE','delete')]
    name = models.CharField(max_length=16, verbose_name='用例名')
    req_method = models.CharField(max_length=6, choices=case_method_choice, default=case_method_choice[0])
    createtime = models.DateTimeField(auto_now_add=True)
    createby = models.ForeignKey(user, null=True, on_delete=models.SET_NULL, related_name='casecreater')
    updatetime = models.DateTimeField(auto_now=True)
    updateby = models.ForeignKey(user, null=True, on_delete=models.SET_NULL, related_name='caseupdater')
    pass


class Case_Source_RouteParam(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='myCSRP')
    param = models.ForeignKey(RouteParams, null=True, on_delete=models.SET_NULL)
    value = models.ForeignKey(SourceResult, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('case', 'param', 'value')


class Case_Source_RouteResponse(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='myCSRR')
    param = models.ForeignKey(RouteParams, null=True, on_delete=models.SET_NULL)
    value = models.ForeignKey(SourceResult, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('case', 'param', 'value')
# class result(models.Model):
#     pass
