# Generated by Django 2.2.1 on 2019-07-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0010_remove_task_jenkins_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='fixed',
            field=models.CharField(choices=[(0, 'error'), (1, 'normal')], default=1, max_length=1),
        ),
    ]