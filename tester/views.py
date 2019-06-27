from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Route, Case, Task
from .pagination import PagePagination
from .serializers import RouteSerializer, RouteListSerializer, CaseSerializer, CaseListSerializer, TaskSerializer, \
    TaskListSerializer

from JenkinsServer.JenkinsServer import Jenkins
from JenkinsServer.JobTemplate import JobConfig


# Create your views here.
class RouteViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    parser_classes = (JSONParser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('project',)
    search_fields = ('name',)
    ordering_fields = ('name', 'route')
    ordering = ('id')
    pagination_class = PagePagination

    # serializer_class = RouteSerializer
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RouteListSerializer
        else:
            return RouteSerializer

    # def get_queryset(self):
    #     queryset = self.queryset.filter(**self.request.query_params)
    #     return queryset


class CaseViewset(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    filterset_fields = ('project',)
    pagenation_class = PagePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CaseListSerializer
        else:
            return CaseSerializer


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    # parser_classes = (JSONParser,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('name', 'jenkins_job',)
    ordering_fields = ('name',)
    ordering = ('id',)
    pagination_class = PagePagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TaskListSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            job = JobConfig()
            job.set_description(request.data.description)
            job.set_run_time(request.data.pop('run_time'))
            job.set_command(request.data.pop('command'))
            jenkins = Jenkins().CreateJenkinsServer()
            jenkins.create_job(request.data.name, job)
        except Exception as e:
            return Response(exception=True, status=404, data={'Detail':'创建jenkins服务失败,错误信息：%s'%e})

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(headers=headers, data=serializer.data, status=201)
