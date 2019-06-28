from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import jenkins

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        err_msg=None

        try:
            job = JobConfig(**request.data)
            # server = jenkins.Jenkins(url='http://127.0.0.1:8080', username='lzd', password='19950223')
            server = Jenkins().CreateJenkinsServer()
            server.create_job(request.data.get('name'), job())
        except Exception as e:
            err_msg=e
        finally:
            server.quiet_down()

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(headers=headers, data=serializer.data, status=201) if not err_msg else Response(exception=True, status=404, data={'Detail': '创建jenkins服务失败,错误信息：%s' % err_msg})
