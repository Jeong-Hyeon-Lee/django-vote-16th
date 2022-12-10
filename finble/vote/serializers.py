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

    class Meta:
        model = User
        fields = ['id', 'team', 'email', 'part', 'name', 'password']

    def create(self, validated_data):
        id = validated_data.get('id')
        team = validated_data.get('team')
        email = validated_data.get('email')
        part = validated_data.get('part')
        name = validated_data.get('name')
        password = validated_data.get('password')
        user = User(
            id=id,
            team=team,
            email=email,
            part=part,
            name=name,
            password=password
        )
        user.set_password(password)
        user.save()
        return user


# class LoginSerializer(serializers.Serializer):
#     id = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True)
#
#     def validate(self, request):
#         id = request.get('id', None)
#         password = request.get('password', None)
#
#         if User.objects.filter(id=id).exists():
#             user = User.objects.get(id=id)
#             if not user.check_password(password):
#                 raise serializers.ValidationError({"Wrong Password"})
#         else:
#             raise serializers.ValidationError({"User doesn't exist."})
#
#         token = RefreshToken.for_user(user)
#         refresh = str(token)
#         access = str(token.access_token)
#
#         data = {
#             'id': user.id,
#             'refresh': refresh,
#             'access': access
#         }
#
#         return data
