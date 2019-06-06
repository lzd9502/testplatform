from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin, NestedUpdateMixin, NestedCreateMixin
from .models import Route, RouteParams, RouteResponseGroup, ResponseGroupParam
from testenvconfig.models import Project


class RouteParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteParams
        fields = ('id', 'param', 'datatype')


class RouteListSerializer(serializers.ModelSerializer):
    myrouteparams = RouteParamSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        # fields='__all__'
        exclude = ['project']


class RouteSerializer(WritableNestedModelSerializer):
    myrouteparams = RouteParamSerializer(many=True)

    class Meta:
        model = Route
        # exclude=['project']
        fields = '__all__'
        validators = [UniqueTogetherValidator(queryset=Route.objects.all(),fields=('name','project'),message='该项目下已有同名路由！')]
    # def create(self, validated_data):
    #     myrouteparams_data=validated_data.pop('myrouteparams')
    #     route=Route.objects.create(**validated_data)
    #     RouteParams.objects.create(route=route.id,**myrouteparams_data)
    #     return route

