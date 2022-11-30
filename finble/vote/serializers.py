from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import *


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = ['created_at', 'updated_at', 'deleted_at']


class TeamSerializer(BaseModelSerializer):
    class Meta:
        model = Team
        fields = ['team_id', 'name', 'vote_num']


class UserSerializer(BaseModelSerializer):
    team = TeamSerializer

    class Meta:
        model = User
        fields = ['id', 'team', 'email', 'password', 'part', 'name', 'part_voted', 'demo_voted', 'vote_num']


class JoinSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'team', 'email', 'password', 'part', 'name')

    def save(self, request):
        user = User.objects.create_user(
            id=self.validated_data['id'],
            team=self.validated_data['team'],
            email=self.validated_data['email'],
            part=self.validated_data['part'],
            name=self.validated_data['name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, request):
        id = request.get('id', None)
        password = request.get('password', None)

        if User.objects.filter(id=id).exists():
            user = User.objects.get(id=id)
            if not user.check_password(password):
                raise serializers.ValidationError({"Wrong Password"})
        else:
            raise serializers.ValidationError({"User doesn't exist."})

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'id': user.id,
            'refresh': refresh,
            'access': access
        }

        return data
