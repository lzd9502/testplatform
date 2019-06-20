from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested import WritableNestedModelSerializer
from .models import DataSource,SourceResult

class SourceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=SourceResult
        fields=('id','name',)


class DataSourceSerializer(WritableNestedModelSerializer):
    children=SourceResultSerializer(many=True)
    class Meta:
        model=DataSource
        fields='__all__'
        validator=[UniqueTogetherValidator(queryset=SourceResult.objects.all(),fields=('name','datasource'),message='存在同名的结果变量！')]
