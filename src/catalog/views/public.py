from rest_framework import permissions
from rest_framework.generics import ListAPIView

from catalog.models import Genre, Category
from catalog.serializers import GenreUserSerializer, CategoryUserSerializer


class PublicGenreListAPIView(ListAPIView):
    queryset = Genre.objects.filter(is_active=True)
    serializer_class = GenreUserSerializer
    permission_classes = (permissions.AllowAny,)


class PublicCategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryUserSerializer
    permission_classes = (permissions.AllowAny,)
