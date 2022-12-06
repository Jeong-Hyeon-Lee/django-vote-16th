from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class JoinView(APIView):
    serializer_class = JoinSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "email": user.email,
                    "nickname": user.nickname,
                    "message": "가입이 성공적으로 이뤄졌습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            id = serializer.validated_data['id']
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            # data = serializer.validated_data
            res = Response(
                {
                    "message": "로그인되었습니다.",
                    "id": id,
                    "access": access,
                    "refresh": refresh
                },
                status=status.HTTP_200_OK,
            )
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteResult(APIView):
    def get(self, request, part):
        candidates = User.objects.filter(part=part)
        serializer = UserSerializer(candidates, many=True)
        return Response(serializer.data)

    def patch(self, request, part):
        voting_user_instance = get_object_or_404(User, id=request.user)
        serializer1 = UserSerializer(instance=voting_user_instance, data={"part_voted": True})
        voted_user_instance = get_object_or_404(User, id=request.data)
        serializer2 = UserSerializer(instance=voted_user_instance, data={"vote_num": voted_user_instance.vote_num + 1})
        if serializer1.is_valid():
            if serializer2.is_valid():
                serializer1.save()
                serializer2.save()
                return Response(serializer2.data, status=201)
            return Response(serializer1.errors, status=400)
        return Response(serializer2.errors, status=400)
