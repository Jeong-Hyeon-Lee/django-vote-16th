from django.contrib.auth import authenticate
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
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "가입이 성공적으로 이루어졌습니다",
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
    def post(self, request):
        user = authenticate(
            id=request.data.get("id"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인에 성공했습니다",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response({"존재하지 않는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)


class VoteResult(APIView):
    def get(self, request, part):
        candidates = User.objects.filter(part=part)
        serializer = UserSerializer(candidates, many=True)
        return Response(serializer.data)

    def patch(self, request, part):
        voting_user_instance = get_object_or_404(User, id=self.request.user)
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


