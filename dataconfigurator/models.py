from django.db import models
from testenvconfig.models import Project

# Create your models here.

DATASOURCE_TYPE_CHOICE = ((0, 'sql'), (1, 'fix'), (2, 'function'))


class DataSource(models.Model):
    name = models.CharField(max_length=64, verbose_name='源名')
    source_type = models.CharField(max_length=1, choices=DATASOURCE_TYPE_CHOICE, default=1, verbose_name='数据源形式')
    source_runner = models.TextField(max_length=500, verbose_name='源数据获取器')
    source_creater = models.TextField(max_length=500, null=True,blank=True,verbose_name='源数据生成器')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='mydatasource')


class SourceResult(models.Model):
    name = models.CharField(max_length=64, verbose_name='结果名')
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='children')
