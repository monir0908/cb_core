from django.urls import path

from catalog.views.users import (
    UserGenreListAPIView,
    UserCategoryListAPIView
)

app_name = 'user.catalog'

urlpatterns = [
    path('categories', UserCategoryListAPIView.as_view(), name='users.category.list.api'),
    path('genre', UserGenreListAPIView.as_view(), name='users.genre.list.api'),
]
