from django.urls import path

from user.views import UserRetrieveUpdateAPIView

app_name = 'user'

urlpatterns = [
    path('users/<str:username>', UserRetrieveUpdateAPIView.as_view()),
]
