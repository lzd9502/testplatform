from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested import WritableNestedModelSerializer

from dataconfigurator.serializers import SourceResultSerializer
from .models import Route, RouteParams, RouteResponseGroup, ResponseGroupParam, Case, Case_Source_RouteParam, \
    Case_Source_RouteResponse, Task, Task2Case
from testenvconfig.models import Project
from testenvconfig.serializers import UserSerializer


# ================================================================
# -------------------------------Route----------------------------
# ================================================================
class RouteParamSerializer(serializers.ModelSerializer):
    data_type = serializers.SerializerMethodField()

    def get_data_type(self, obj):
        return obj.get_data_type_display()

    class Meta:
        model = RouteParams
        fields = ('id', 'param', 'data_type')


class ResponseParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseGroupParam
        fields = ('id', 'param')


class ResponseParams4CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseGroupParam
        fields = '__all__'


# class RouteResponseSerializer(serializers.ModelSerializer):
#     mygroupparams = ResponseParamsSerializer(many=True)
#
#     class Meta:
#         model = RouteResponseGroup
#         # fields = '__all__'
#         exclude=['route']
#         validators = [UniqueTogetherValidator(queryset=RouteResponseGroup.objects.all(),fields=('route','name'),message='同一路由下响应组名称不能相同')]
#     def create(self, validated_data):
#         mygroupparams_data=validated_data.pop('mygroupparams')
#         group=RouteResponseGroup.objects.create(**validated_data)
#         for mygroupparam_data in mygroupparams_data:
#             ResponseGroupParam.objects.create(Group=group,**mygroupparam_data)
#         return group
class RouteResponseSerializer(WritableNestedModelSerializer):
    mygroupparams = ResponseParamsSerializer(many=True)

    class Meta:
        model = RouteResponseGroup
        fields = ('id', 'name', 'mygroupparams')
        # todo:这里的验证怎么处理，联合唯一，使用WritableNested序列化器无法通过valid
        # validators = [UniqueTogetherValidator(queryset=RouteResponseGroup.objects.all(),fields=('route','name'),message='同一路由下响应组名称不能相同')]


class RouteListSerializer(serializers.ModelSerializer):
    myrouteparams = RouteParamSerializer(many=True, read_only=True)
    myresponsegroup = RouteResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        exclude = ['project']


# class RouteSerializer(serializers.ModelSerializer):
#     myrouteparams = RouteParamSerializer(many=True)
#     myresponsegroup = RouteResponseSerializer(many=True)
#
#     class Meta:
#         model = Route
#         fields = ('id','project','name','route','myrouteparams','myresponsegroup')
#         validators = [
#             UniqueTogetherValidator(queryset=Route.objects.all(), fields=('name', 'project'), message='该项目下已有同名路由！')]
#
#     def create(self, validated_data):
#         myrouteparams_data=validated_data.pop('myrouteparams')
#         myresponsegroup_datas=validated_data.pop('myresponsegroup')
#         route=Route.objects.create(**validated_data)
#         for myrouteparam_data in myrouteparams_data:
#             RouteParams.objects.create(route=route,**myrouteparam_data)
#         for myresponsegroup_data in myresponsegroup_datas:
#             RouteResponseGroup.objects.create(route=route,**myresponsegroup_data)
#         return route
class RouteSerializer(WritableNestedModelSerializer):
    myrouteparams = RouteParamSerializer(many=True)
    myresponsegroup = RouteResponseSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=Route.objects.all(), fields=('name', 'project'), message='该项目下已有同名路由！'),
            UniqueTogetherValidator(queryset=RouteResponseGroup.objects.all(), fields=('route', 'name'),
                                    message='同一路由下响应组名称不能相同')]


# ================================================================
# -------------------------------Case-----------------------------
# ================================================================


class CSRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case_Source_RouteParam
        fields = ('id', 'route_param', 'data_source',)


class CSRPListSerializer(serializers.ModelSerializer):
    route_param = RouteParamSerializer()
    data_source = SourceResultSerializer()

    class Meta:
        model = Case_Source_RouteParam
        fields = ('id', 'route_param', 'data_source',)


class CSRRSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Case_Source_RouteResponse
        fields = ('id', 'response', 'data_source',)


class CSRRListSerializer(WritableNestedModelSerializer):
    response = ResponseParams4CaseSerializer()
    data_source = SourceResultSerializer()

    class Meta:
        model = Case_Source_RouteResponse
        fields = ('id', 'response', 'data_source',)


class CaseListSerializer(serializers.ModelSerializer):
    req_method = serializers.CharField(source='get_req_method_display')
    myCSRP = CSRPListSerializer(many=True)
    myCSRR = CSRRListSerializer(many=True)
    createby = UserSerializer()
    updateby = UserSerializer()

    class Meta:
        model = Case
        exclude = ['project', ]


class CaseSerializer(WritableNestedModelSerializer):
    myCSRP = CSRPSerializer(many=True)
    myCSRR = CSRRSerializer(many=True)

    # myCSRR = ResponseParams4CaseSerializer(many=True)

    class Meta:
        model = Case
        fields = '__all__'


# ================================================================
# -------------------------------Task-----------------------------
# ================================================================

class Task2CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task2Case
        fields = ('case', 'disabled')


class Task2CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task2Case
        exclude=('task',)


class TaskSerializer(WritableNestedModelSerializer):
    myCase = Task2CaseSerializer(many=True, allow_null=True)

    class Meta:
        model = Task
        fields = '__all__'
    # def create(self, validated_data):
    #     print(validated_data)
    #     myCase=validated_data.pop()


class TaskListSerializer(serializers.ModelSerializer):
    myCase = Task2CaseListSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'
