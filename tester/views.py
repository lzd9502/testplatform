from rest_framework import viewsets
from .models import Route
from testenvconfig.models import Project
from .serializers import RouteSerializer,ProjectRouteSerializer


# Create your views here.
class RouteViewset(viewsets.ModelViewSet):
    queryset =Route.objects.all()
    serializer_class = RouteSerializer
    lookup_field = 'project'
    def get_queryset(self):
       queryset=self.queryset.filter(**self.request.query_params)
       return queryset
# class RouteViewset(viewsets.ModelViewSet):
#     queryset =Project.objects.all()
#     serializer_class = ProjectRouteSerializer
#     # def get_queryset(self):
#     #     print(self.request)
#     #     queryset=Project.objects.filter(self.request.id)
#     #     return queryset
