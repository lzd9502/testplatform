from django.db import models
from testenvconfig.models import Project

# Create your models here.
class DataSource(models.Model):
    type_choice = ((0, 'sql'), (1, 'fix'), (2, 'function'))
    name = models.CharField(max_length=16, verbose_name='源名')
    source_type = models.CharField(max_length=1,choices=type_choice, default=1, verbose_name='数据源形式')
    source_value_runner = models.TextField(max_length=500, verbose_name='源数据获取器')
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='mydatasource')


class SourceResult(models.Model):
    name = models.CharField(max_length=16, verbose_name='结果名')
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='children')
