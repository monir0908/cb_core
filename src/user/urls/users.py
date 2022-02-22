from django.urls import path

from user.views import upload_image, ProfileCreateAPIView, ProfileRetrieveUpdateAPIView, RatingReviewListCreateAPIView, UserListAPIView

app_name = 'user'

urlpatterns = [
    path('file-upload', upload_image),
    path('create-profile', ProfileCreateAPIView.as_view()),
    path('user-profile', ProfileRetrieveUpdateAPIView.as_view()),
    path('user-rating', RatingReviewListCreateAPIView.as_view()),
    path('user-list', UserListAPIView.as_view()),
]
