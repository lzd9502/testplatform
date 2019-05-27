from rest_framework import serializers
from .models import U2P, User, Project
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_permissions', 'is_active', 'last_login')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['createtime', 'members']


class U2PSerializer(serializers.ModelSerializer):
    User = serializers.HiddenField(default=serializers.CurrentUserDefault())
    Project=ProjectSerializer()
    class Meta:
        model = U2P
        validators = [UniqueTogetherValidator(
            queryset=U2P.objects.all(),
            fields=('User', 'Project'),
            message="已加入该项目"
        )]
        fields = ('id', 'User', 'Project')


class U2PDetailSerializer(serializers.ModelSerializer):
    Project = ProjectSerializer()

    class Meta:
        model = U2P
        fields = ('id', 'Project')
