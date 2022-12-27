from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

app_name = 'vote'

urlpatterns = [
    path('results/<str:part>/', VoteResult.as_view()),
    path('demo-results/', DemoVoteResult.as_view()),
    path('join/', JoinView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
]
