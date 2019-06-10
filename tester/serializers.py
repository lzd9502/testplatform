from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin, NestedUpdateMixin, NestedCreateMixin

from .models import Route, RouteParams, RouteResponseGroup, ResponseGroupParam
from testenvconfig.models import Project


class RouteParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteParams
        fields = ('id', 'param', 'datatype')


class ResponseParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseGroupParam
        fields = ('pk', 'param')


class RouteResponseSerializer(WritableNestedModelSerializer):
    mygroupparams = ResponseParamsSerializer(many=True)

    class Meta:
        model = RouteResponseGroup
        # fields = '__all__'
        exclude=['route']
        validators = [UniqueTogetherValidator(queryset=RouteResponseGroup.objects.all(),fields=('route','name'),message='同一路由下响应组名称不能相同')]


class RouteListSerializer(serializers.ModelSerializer):
    myrouteparams = RouteParamSerializer(many=True, read_only=True)
    myresponsegroup = RouteResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        exclude = ['project']


class RouteSerializer(WritableNestedModelSerializer):
    myrouteparams = RouteParamSerializer(many=True)
    myresponsegroup = RouteResponseSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=Route.objects.all(), fields=('name', 'project'), message='该项目下已有同名路由！')]
    # def create(self, validated_data):
    #     myrouteparams_data=validated_data.pop('myrouteparams')
    #     route=Route.objects.create(**validated_data)
    #     RouteParams.objects.create(route=route.id,**myrouteparams_data)
    #     return route
