from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# from drf_yasg.utils import swagger_auto_schema


class JoinView(APIView):
    serializer_class = JoinSerializer
    permission_classes = [AllowAny]

    # @swagger_auto_schema(tags=['회원가입'], query_serializer=JoinBodySerializer, responses={200: 'Success'})
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
    permission_classes = [AllowAny]

    # @swagger_auto_schema(tags=['로그인'], query_serializer=LoginBodySerializer, responses={200: 'Success'})
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refresh')
        return response


class VoteResult(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, part):
        candidates = User.objects.filter(part=part).order_by('-vote_num')
        serializer = UserSerializer(candidates, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(tags=['파트장 투표'], query_serializer=VoteBodySerializer, responses={200: 'Success'})
    def patch(self, request, part):
        voting_user_instance = get_object_or_404(User, id=request.user.id)
        voted_user_instance = get_object_or_404(User, id=request.data['id'])

        if voting_user_instance.part_voted:
            return Response({"이미 투표한 사용자입니다."}, status=status.HTTP_200_OK)

        if voting_user_instance.part != voted_user_instance.part:
            return Response({"자신의 파트에만 투표할 수 있습니다."}, status=status.HTTP_200_OK)

        if voting_user_instance == voted_user_instance:
            serializer = UserSerializer(instance=voted_user_instance,
                                        data={"part_voted": True, "vote_num": voted_user_instance.vote_num + 1},
                                        partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        else:
            serializer1 = UserSerializer(instance=voting_user_instance, data={"part_voted": True}, partial=True)
            serializer2 = UserSerializer(instance=voted_user_instance,
                                         data={"vote_num": voted_user_instance.vote_num + 1},
                                         partial=True)
            if serializer1.is_valid():
                if serializer2.is_valid():
                    serializer1.save()
                    serializer2.save()
                    serializer_list = [serializer1.data, serializer2.data]
                    response = {
                        'status': status.HTTP_200_OK,
                        'data': serializer_list,
                    }
                    return Response(response)
                return Response(serializer2.errors, status=400)
            return Response(serializer1.errors, status=400)


class DemoVoteResult(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        candidates = Team.objects.all().order_by('-vote_num').values()
        serializer = TeamSerializer(candidates, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(tags=['데모데이 투표'], query_serializer=DemoVoteBodySerializer, responses={200: 'Success'})
    def patch(self, request):
        voting_user_instance = get_object_or_404(User, id=request.user.id)
        voted_team_instance = get_object_or_404(Team, id=request.data['id'])

        if voting_user_instance.demo_voted:
            return Response({"이미 투표한 사용자입니다."}, status=status.HTTP_200_OK)

        if voting_user_instance.team == voted_team_instance:
            return Response({"본인이 속한 팀에는 투표할 수 없습니다."}, status=status.HTTP_200_OK)

        serializer1 = UserSerializer(instance=voting_user_instance, data={"demo_voted": True}, partial=True)
        serializer2 = TeamSerializer(instance=voted_team_instance,
                                     data={"vote_num": voted_team_instance.vote_num + 1},
                                     partial=True)
        if serializer1.is_valid():
            if serializer2.is_valid():
                serializer1.save()
                serializer2.save()
                serializer_list = [serializer1.data, serializer2.data]
                response = {
                    'status': status.HTTP_200_OK,
                    'data': serializer_list,
                }
                return Response(response)
            return Response(serializer2.errors, status=400)
        return Response(serializer1.errors, status=400)


class Test(APIView):
    def get(self, request):
        res = Response(
            {
                "hello world"
            },
            status=status.HTTP_200_OK,
        )
        return res
