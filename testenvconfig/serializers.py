from rest_framework import serializers
from .models import U2P, User, Project, ProjectConfig
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_permissions', 'is_active', 'last_login')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['createtime', 'members']


class ProjectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectConfig
        exclude=['project']


class U2PSerializer(serializers.ModelSerializer):
    # User = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = U2P
        validators = [UniqueTogetherValidator(
            queryset=U2P.objects.all(),
            fields=('User', 'Project'),
            message="已加入该项目"
        )]
        fields = ('id', 'User', 'Project')
