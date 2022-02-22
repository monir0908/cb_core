from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from payment.tasks import decrease_user_balance
from post.filters import PostFilters
from post.models import Post, PostConfig
from post.serializers import PostSerializer, PostConfigSerializer


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def approve_post(request, slug: str) -> Response:
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise ValidationError('post does not exists', code=status.HTTP_404_NOT_FOUND)
    if post.status == Post.Statuses.APPROVED:
        raise ValidationError('post is already approved', code=status.HTTP_400_BAD_REQUEST)
    post.status = Post.Statuses.APPROVED
    post.updated_by = request.user
    post.save()
    decrease_user_balance.delay(updated_by=request.user.username, post_slug=post.slug)
    return Response(data=PostSerializer(post).data, status=status.HTTP_200_OK)


class AdminPostListAPIView(ListAPIView):
    queryset = Post.objects.select_related('category', 'genre').filter()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilters


class AdminPostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.select_related('category', 'genre').filter()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ['patch', 'get']

    def patch(self, request, *args, **kwargs):
        request.data['updated_by_id'] = self.request.user.id
        return super(AdminPostRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)


class AdminPostConfigListAPIView(ListAPIView):
    queryset = PostConfig.objects.all()
    serializer_class = PostConfigSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AdminPostConfigRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = PostConfig.objects.all()
    serializer_class = PostConfigSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ('patch', 'get',)

    def patch(self, request, *args, **kwargs):
        request.data['updated_by_id'] = self.request.user.id
        return super(AdminPostConfigRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)
