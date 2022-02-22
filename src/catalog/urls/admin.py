from django.urls import path

from catalog.views.admin import (
    AdminCategoryListCreateAPIView,
    AdminGenreListCreateAPIView,
    AdminCategoryRetrieveUpdateAPIView,
    AdminGenreRetrieveUpdateAPIView,
    bulk_upload_genre_and_category
)

app_name = 'admin.catalog'

urlpatterns = [
    path('categories', AdminCategoryListCreateAPIView.as_view(), name='admin.category.list.create.api'),
    path('categories/<str:slug>', AdminCategoryRetrieveUpdateAPIView.as_view(), name='admin.category.get.update.api'),
    path('genre', AdminGenreListCreateAPIView.as_view(), name='admin.genre.list.update.api'),
    path('genre/<str:slug>', AdminGenreRetrieveUpdateAPIView.as_view(), name='admin.genre.get.update.api'),
    path('bulk-upload', bulk_upload_genre_and_category, name='admin.genre.category.bulk.upload.api'),
]
