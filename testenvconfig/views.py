from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from testenvconfig.models import U2P, Project,User
from testenvconfig.serializers import U2PSerializer,  ProjectSerializer,UserSerializer


# Create your views here.
class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class UserInfoViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.get(self.request.user)
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer_class()
        res=get_object_or_404(queryset)
        ser=serializer(queryset)
        return Response(ser.data)
class UserProjectViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    def get_queryset(self):
        return U2P.objects.filter(User=self.request.user)

    def get_serializer_class(self):
        # if self.action == 'list':
        #     return U2PDetailSerializer
        return U2PSerializer

    def retrieve(self, request, **kwargs):
        queryset = self.get_queryset()
        res = get_object_or_404(queryset, **kwargs)
        serializer = self.get_serializer_class()
        ser = serializer(res)
        return Response(ser.data)
