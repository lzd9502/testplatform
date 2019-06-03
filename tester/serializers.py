from rest_framework import serializers
from .models import Route,RouteParams,RouteResponseGroup,ResponseGroupParam

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Route
        fields=('')
