from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from testenvconfig.models import U2P
from testenvconfig.serializers import U2PSerializer, U2PDetailSerializer


# Create your views here.
class UserinfoViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    lookup_field = 'Project_id'

    def get_queryset(self):
        return U2P.objects.filter(User=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return U2PDetailSerializer
        return U2PSerializer

    # def retrieve(self, request, **kwargs):
    #     queryset = self.get_queryset()
    #     res = get_object_or_404(queryset,**kwargs)
    #     serializer = self.get_serializer_class()
    #     ser = serializer(res)
    #     return Response(ser.data)
