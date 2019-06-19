from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Route, Case
from .pagination import PagePagination
from .serializers import RouteSerializer, RouteListSerializer, CaseSerializer, CaseListSerializer


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
    search_fields = ('name')
    pagenation_class = PagePagination
    def get_serializer_class(self):
        if self.action == 'list':
            return CaseListSerializer
        else:
            return CaseSerializer
