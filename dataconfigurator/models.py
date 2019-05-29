from django.db import models
from tester.models import case

# Create your models here.
class datasource(models.Model):
    type_choice=[(0,'sql'),(1,'fix'),(2,'function')]
    name=models.CharField(max_length=16,verbose_name='源名')
    sourcetype=models.CharField(choices=type_choice,default=1,verbose_name='数据源形式')
    value=models.TextField(max_length=500,verbose_name='源值')

    pass
class case2source(models.Model):

    case=models.ForeignKey(case,on_delete=models.CASCADE)
    datasource=models.ForeignKey(datasource,on_delete=models.CASCADE)

