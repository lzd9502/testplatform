from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DataSource
from .serializers import DataSourceSerializer

# Create your views here.
class DataSourceViewset(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    filter_backends = (filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend)
    search_fields=('name',)
    ordering_fields=('name',)
    filterset_fields=('project',)
