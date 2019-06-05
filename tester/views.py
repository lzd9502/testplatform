from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from .models import Route
from testenvconfig.models import Project
from .serializers import RouteSerializer, RouteListSerializer, ProjectRouteSerializer


# Create your views here.
class RouteViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    parser_classes = (JSONParser,FormParser,MultiPartParser)

    # serializer_class = RouteSerializer
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RouteListSerializer
        else:
            return RouteSerializer

    def create(self, request, *args, **kwargs):
        print(list(request.data['myrouteparams']))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # def get_queryset(self):
    #     queryset = self.queryset.filter(**self.request.query_params)
    #     return queryset
# class RouteViewset(viewsets.ModelViewSet):
#     queryset =Project.objects.all()
#     serializer_class = ProjectRouteSerializer
#     lookup_field = 'id'
# def get_queryset(self):
#     print(self.request.query_params)
#     queryset=Project.objects.filter(self.request.query_params)
#     return queryset
