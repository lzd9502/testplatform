# Generated by Django 2.2.1 on 2019-08-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0015_auto_20190806_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(max_length=64, verbose_name='用例名'),
        ),
        migrations.AlterField(
            model_name='responsegroupparam',
            name='param',
            field=models.CharField(max_length=64, verbose_name='参数名'),
        ),
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.CharField(max_length=8, verbose_name='success,skip,err,fail'),
        ),
        migrations.AlterField(
            model_name='route',
            name='name',
            field=models.CharField(max_length=64, verbose_name='routeName'),
        ),
        migrations.AlterField(
            model_name='route',
            name='route',
            field=models.CharField(max_length=128, verbose_name='route'),
        ),
        migrations.AlterField(
            model_name='routeparams',
            name='param',
            field=models.CharField(max_length=64, verbose_name='参数名'),
        ),
        migrations.AlterField(
            model_name='routeresponsegroup',
            name='name',
            field=models.CharField(max_length=64, verbose_name='responseGroupName'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='任务名称'),
        ),
    ]
