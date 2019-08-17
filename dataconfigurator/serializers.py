from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested import WritableNestedModelSerializer
from .models import DataSource, SourceResult


class SourceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceResult
        fields = ('id', 'name',)


class DataSourceSerializer(WritableNestedModelSerializer):
    children = SourceResultSerializer(many=True)

    class Meta:
        model = DataSource
        fields = '__all__'
        validators = [UniqueTogetherValidator(queryset=DataSource.objects.all(), fields=('name', 'project'),
                                             message='the same datasource in your project'),
                      # UniqueTogetherValidator(queryset=SourceResult.objects.all(),fields=('name','datasource'),message='same datasource with children')
        ]


class DataSourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'


class SourceResultListSerializer(serializers.ModelSerializer):
    datasource = DataSourceListSerializer()

    class Meta:
        model = SourceResult
        fields = '__all__'
