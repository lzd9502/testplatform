from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Route,RouteParams,RouteResponseGroup,ResponseGroupParam
from testenvconfig.models import Project

class RouteParamSerializer(serializers.ModelSerializer):
    class Meta:
        model=RouteParams
        exclude=['route']
class RouteSerializer(WritableNestedModelSerializer):
    myrouteparams=RouteParamSerializer(many=True)
    class Meta:
        model=Route
        exclude=['project']
    # def create(self, validated_data):
    #     myrouteparams_data=validated_data.pop('myrouteparams')
    #     route=Route.objects.create(**validated_data)
    #     RouteParams.objects.create(route=route.id,**myrouteparams_data)
    #     return route

class ProjectRouteSerializer(WritableNestedModelSerializer):
    myroute=RouteSerializer(many=True)
    class Meta:
        model=Project
        fields=('id','myroute')