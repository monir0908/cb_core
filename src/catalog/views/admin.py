from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from catalog.models import Category, Genre
from catalog.serializers import CategoryAdminSerializer, GenreAdminSerializer
from catalog.tasks import bulk_upload_category_genre
from catalog.utils import slugify


class AdminCategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategoryAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if not request.data.get('name'):
            raise ValidationError(detail='name key is required', code=status.HTTP_400_BAD_REQUEST)
        request.data['slug'] = slugify(request.data['name'])
        request.data['created_by'] = self.request.user.id
        return super(AdminCategoryListCreateAPIView, self).create(request, *args, **kwargs)


class AdminGenreListCreateAPIView(ListCreateAPIView):
    queryset = Genre.objects.filter()
    serializer_class = GenreAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if not request.data.get('name'):
            raise ValidationError(detail='name key is required', code=status.HTTP_400_BAD_REQUEST)
        request.data['slug'] = slugify(request.data['name'])
        request.data['created_by'] = self.request.user.id
        return super(AdminGenreListCreateAPIView, self).create(request, *args, **kwargs)


class AdminGenreRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Genre.objects.filter()
    serializer_class = GenreAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ['patch', 'get']

    def patch(self, request, *args, **kwargs):
        request.data['updated_by_id'] = self.request.user
        return super(AdminGenreRetrieveUpdateAPIView, self).update(request, *args, **kwargs)


class AdminCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategoryAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ['patch', 'get']

    def patch(self, request, *args, **kwargs):
        request.data['updated_by_id'] = self.request.user
        return super(AdminCategoryRetrieveUpdateAPIView, self).update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_upload_genre_and_category(request: Request) -> Response:
    if not request.data.get('email') or not request.data.get('type'):
        raise ValidationError('email or/and file type is missing', code=status.HTTP_400_BAD_REQUEST)
    if request.data.get('type') == 'category':
        pass
    elif request.data.get('type') == 'genre':
        pass
    else:
        raise ValidationError(detail='wrong type value', code=status.HTTP_400_BAD_REQUEST)
    bulk_upload_category_genre.delay(request.data['email'], request.data['url'],
                                     request.user.username, request.data['type'])
    return Response(data={'message': 'your uploaded file is processing'}, status=status.HTTP_201_CREATED)
