from django.urls import path

from catalog.views.public import (
    PublicGenreListAPIView,
    PublicCategoryListAPIView
)

app_name = 'public.catalog'

urlpatterns = [
    path('categories', PublicCategoryListAPIView.as_view(), name='public.category.list.api'),
    path('genre', PublicGenreListAPIView.as_view(), name='public.genre.list.api'),
]
