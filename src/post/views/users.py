import string
import random
import datetime

from django.db.models import Q
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework import permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, get_object_or_404
from rest_framework.exceptions import ValidationError

from catalog.models import Category, Genre
from catalog.utils import slugify
from post.filters import PostFilters
from post.models import Post, PostInterest, PostSize, PostComment, PostBookmark, SettlePost
from post.serializers import (
    PostSerializer,
    PostInterestSerializer,
    PostBookMarkSerializer,
    PostCommentSerializer,
    PostSettleSerializer
)
from post.tasks import increase_interest_count, increase_settlement_count
from post.utils import identifier_builder, get_pay_as_you_go_config, get_premium_config
from user.models import User
from user.permissions import IsApprovedUser


class UserPostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.select_related('category', 'genre').filter()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilters

    def create(self, request, *args, **kwargs) -> Response:
        category = get_object_or_404(Category, slug=request.data['category'])
        genre = get_object_or_404(Genre, slug=request.data['genre'])
        request.data['category'] = category.id
        request.data['genre'] = genre.id
        print(request.data['genre'], request.data['category'])
        if not self.request.user.is_approved:
            raise ValidationError(detail='user is not approved', code=status.HTTP_400_BAD_REQUEST)
        waited_post = Post.objects.filter(created_by=self.request.user, status=Post.Statuses.WAITED)
        if waited_post:
            raise ValidationError('there is a post waiting for approval', code=status.HTTP_400_BAD_REQUEST)
        request.data['username'] = self.request.user.username
        request.data['identifier'] = identifier_builder()
        random_chars = ''.join(k for k in random.choices(string.ascii_lowercase, k=5))
        request.data['slug'] = slugify(request.data.get('title')) + '-' + random_chars
        request.data['created_by'] = self.request.user.id
        if request.data.get('is_drafted'):
            request.data['status'] = Post.Statuses.DRAFTED
        else:
            request.data['status'] = Post.Statuses.WAITED
        if isinstance(request.data.get('images'), list) and len(request.data.get('images')) > 5:
            raise ValidationError(detail='you can choose at most 3 images', code=status.HTTP_400_BAD_REQUEST)
        if request.data.get('minimum_order_quantity') and request.data.get('quantity'):
            if request.data['minimum_order_quantity'] > request.data['quantity']:
                raise ValidationError(detail='minimum order quantity cannot be more than quantity',
                                      code=status.HTTP_400_BAD_REQUEST)
        if self.request.user.is_premium:
            request.data['live_time'] = get_premium_config()
            request.data['points_needed'] = 0
        else:
            request.data['live_time'], request.data['points_needed'] = get_pay_as_you_go_config(request.data['package'])
            if self.request.user.balance < request.data['points_needed']:
                raise ValidationError('you do not have sufficient balance', code=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post = serializer.save()
            if request.data.get('size') and isinstance(request.data['size'], list):
                sizes = []
                for size in request.data['size']:
                    sizes.append(PostSize(post=post, value=size, created_by=request.user))
                PostSize.objects.bulk_create(sizes)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserPostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.select_related('category', 'genre').filter()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ['patch', 'get']

    def patch(self, request, *args, **kwargs):
        if not self.request.user.is_approved:
            raise ValidationError(detail='user is not approved', code=status.HTTP_400_BAD_REQUEST)
        existing_post: Post = self.get_object()
        if existing_post.username != self.request.user.username:
            raise ValidationError(detail='you are not the owner', code=status.HTTP_400_BAD_REQUEST)
        if existing_post.status == Post.Statuses.APPROVED:
            raise ValidationError(detail='you cannot update an approved post', code=status.HTTP_400_BAD_REQUEST)
        if isinstance(request.data.get('images'), list) and len(request.data.get('images')) > 5:
            raise ValidationError(detail='you can choose at most 3 images', code=status.HTTP_400_BAD_REQUEST)
        if request.data.get('is_drafted'):
            request.data['status'] = Post.Statuses.DRAFTED
        else:
            waited_post = Post.objects.filter(created_by=self.request.user, status=Post.Statuses.WAITED)
            if waited_post:
                raise ValidationError('there is a post waiting for approval', code=status.HTTP_400_BAD_REQUEST)
            request.data['status'] = Post.Statuses.WAITED
        if request.data.get('minimum_order_quantity') and request.data.get('quantity'):
            if request.data['minimum_order_quantity'] > request.data['quantity']:
                raise ValidationError(detail='minimum order quantity cannot be more than quantity',
                                      code=status.HTTP_400_BAD_REQUEST)
        if request.data.get('live_time'):
            request.data['points_needed'] = request.data.get('live_time', 0) * 10  # todo: points per day from settings
        request.data['updated_by_id'] = self.request.user.id
        return super(UserPostRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)


class UserPostInterestListCreateAPIView(ListCreateAPIView):
    serializer_class = PostInterestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return PostInterest.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_approved:
            raise ValidationError(detail='user is not approved', code=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(slug=request.data['slug'], status=Post.Statuses.PUBLISHED)
        except Post.DoesNotExist:
            raise ValidationError(detail='post not found', code=status.HTTP_404_NOT_FOUND)
        if self.request.user.username == post.username:
            raise ValidationError(detail='you cannot show interest on your own post', code=status.HTTP_400_BAD_REQUEST)
        try:
            PostInterest.objects.get(post=post, username=self.request.user.username)
            raise ValidationError(detail='post is already interested', code=status.HTTP_400_BAD_REQUEST)
        except PostInterest.DoesNotExist:
            request.data['post'] = post.id
            request.data['username'] = self.request.user.username
            request.data['name'] = f'{self.request.user.first_name} {self.request.user.last_name}'
            request.data['created_by'] = self.request.user.id
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                increase_interest_count.delay(post.slug)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserPostBookListCreateAPIView(ListCreateAPIView):
    serializer_class = PostBookMarkSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return PostBookmark.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_approved:
            raise ValidationError(detail='user is not approved', code=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(slug=request.data['slug'], status=Post.Statuses.PUBLISHED)
        except Post.DoesNotExist:
            raise ValidationError(detail='post not found', code=status.HTTP_404_NOT_FOUND)
        if self.request.user.username == post.username:
            raise ValidationError(detail='you cannot bookmark your own post', code=status.HTTP_400_BAD_REQUEST)
        try:
            PostBookmark.objects.get(post=post, username=self.request.user.username)
            raise ValidationError(detail='post is already interested', code=status.HTTP_400_BAD_REQUEST)
        except PostBookmark.DoesNotExist:
            request.data['post'] = post.id
            request.data['username'] = self.request.user.username
            request.data['name'] = f'{self.request.user.first_name} {self.request.user.last_name}'
            request.data['created_by'] = self.request.user.id
            return super(UserPostBookListCreateAPIView, self).create(request, *args, **kwargs)


class UserPostBookRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = PostBookMarkSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'
    http_method_names = ['get', 'delete']

    def get_object(self):
        try:
            return PostBookmark.objects.get(post__slug=self.kwargs['slug'], created_by=self.request.user)
        except PostBookmark.DoesNotExist:
            raise ValidationError(detail='bookmarked post not found', code=status.HTTP_404_NOT_FOUND)


class UserPostCommentListCreateApiView(ListCreateAPIView):
    queryset = PostComment.objects.filter()
    serializer_class = PostCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

    def get_queryset(self):
        return PostComment.objects.filter(post__slug__exact=self.kwargs[self.lookup_field])

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_approved:
            raise ValidationError(detail='user is not approved', code=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(slug=self.kwargs[self.lookup_field], status=Post.Statuses.PUBLISHED)
        except Post.DoesNotExist:
            raise ValidationError(detail='post not found', code=status.HTTP_404_NOT_FOUND)
        request.data['post'] = post.id
        request.data['comment'] = request.data.get('comment')
        request.data['created_by'] = request.user.id
        return super(UserPostCommentListCreateApiView, self).create(request, *args, **kwargs)


class UserPostSettleListCreateApiView(ListCreateAPIView):
    serializer_class = PostSettleSerializer
    permission_classes = (permissions.IsAuthenticated, IsApprovedUser)

    def get_queryset(self):
        return SettlePost.objects.filter(Q(created_by=self.request.user) | Q(settled_with=self.request.user))

    def create(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(created_by=self.request.user,
                                    slug__exact=request.data.get('slug'), status=Post.Statuses.PUBLISHED)
        except Post.DoesNotExist:
            try:
                post = Post.objects.get(created_by=self.request.user,
                                        slug__exact=request.data.get('slug'), status=Post.Statuses.UNPUBLISHED)
            except Post.DoesNotExist:
                raise ValidationError('post not found', code=status.HTTP_400_BAD_REQUEST)
        try:
            settle_with = User.objects.get(username__exact=self.request.data.get('settled_with'),
                                           is_approved=True, is_active=True)
        except User.DoesNotExist:
            raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)
        try:
            SettlePost.objects.get(post=post)
            raise ValidationError('post is already settled', code=status.HTTP_400_BAD_REQUEST)
        except SettlePost.DoesNotExist:
            request.data['post'] = post.id
            request.data['settled_with'] = settle_with.id
            request.data['created_by'] = request.user.id
            request.data['settlement_date'] = self.request.data.get('settlement_date')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                increase_settlement_count.delay(self.request.user.username, post.id)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsApprovedUser])
def publish_post(request: Request, slug: str) -> Response:
    try:
        post = Post.objects.get(slug__exact=slug, status__exact=Post.Statuses.APPROVED, created_by=request.user)
    except Post.DoesNotExist:
        raise ValidationError(detail='post not found', code=status.HTTP_404_NOT_FOUND)
    # todo: need to check from payment module
    post.published_at = timezone.now()
    post.unpublished_at = post.published_at + datetime.timedelta(days=post.live_time)
    post.status = Post.Statuses.PUBLISHED
    post.save()
    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


