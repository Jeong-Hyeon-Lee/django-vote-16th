from .views import *
from django.urls import path

app_name = 'vote'

urlpatterns = [
    path('results/<str:part>', VoteResult.as_view()),
    path('results/demo', DemoVoteResult.as_view()),
    path('join/', JoinView.as_view()),
    path('login/', LoginView.as_view()),
]