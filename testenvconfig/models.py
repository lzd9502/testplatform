import time
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=8, verbose_name='用户名', unique=True, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    # permission=models.CharField(choices=)
    def __str__(self):
        return '%s' % self.username


# class ProductGroup(models.Model):
#     name = models.CharField(max_length=20, verbose_name='产品组', )
#     # isenabled=models.BooleanField(default=True,verbose_name='产品状态')
#     createtime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
#
#     def __str__(self):
#         return '%s' % self.name


class Project(models.Model):
    #TODO:members is writeonly,fix it before next migrate
    name = models.CharField(max_length=20, verbose_name='项目', )
    disabled = models.BooleanField(default=True, verbose_name='启用状态')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    members = models.ManyToManyField(User, through='U2P', )

    def __str__(self):
        return '<%s>' % self.name


class U2P(models.Model):
    #TODO:add uniquecode('User','Project')
    User = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    Project = models.ForeignKey(Project, related_name='Project', on_delete=models.CASCADE)
    createtime = models.DateTimeField(auto_now_add=True)

    pass


class ProjectConfig(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, verbose_name='配置名称')
    host = models.GenericIPAddressField(null=False, blank=False, verbose_name='服务端地址')
    port = models.CharField(max_length=10, null=True, blank=True, verbose_name='端口号')
    projectid = models.ForeignKey(to=Project, to_field='id', on_delete=models.CASCADE, related_name='testconfig',
                                  verbose_name='所属项目')

    def __str__(self):
        return '<%s>==><%s>' % (self.name, self.projectid.name)

# class AutoTask(models.Model):
# name = models.CharField(max_length=)
