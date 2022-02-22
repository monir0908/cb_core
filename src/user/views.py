import uuid

from django.conf import settings
from django.db.models import Q

import boto3
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status, filters

from user.filters import UserFilters
from user.rating_serializer import RatingReviewSerializer
from user.serializers import UserProfileSerializers, UserDetailSerializer, UserSerializer
from user.models import UserProfile, User, RatingReview
from user.tasks import increase_rating_value
from post.models import Post, SettlePost


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request: Request) -> Response:
    file = request.FILES.get('file')
    path = request.POST.get('path')
    if not file or not path:
        raise ValidationError(detail='invalid request', code=status.HTTP_400_BAD_REQUEST)
    filename = file.name
    filename = f'{uuid.uuid4().hex}-{filename}'
    key = f'{path}/{filename}'
    content = file.read()
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.SECRET_ACCESS_KEY,
                             region_name='ap-southeast-1')
    s3_client.put_object(
        Body=content,
        Bucket=settings.S3_BUCKET,
        Key=key,
    )
    host = f'https://{settings.S3_BUCKET}.s3.amazonaws.com'
    res = {
        'url': f'{host}/{key}'
    }
    return Response(data=res, status=status.HTTP_201_CREATED)


class ProfileCreateAPIView(CreateAPIView):
    serializer_class = UserProfileSerializers
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super(ProfileCreateAPIView, self).create(request, *args, **kwargs)


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_approved=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = UserFilters


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializers
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.filter()
    http_method_names = ['patch', 'get']

    def get_object(self):
        try:
            return UserProfile.objects.get(user__username=self.request.user.username)
        except UserProfile.DoesNotExist:
            raise ValidationError(detail='user profile not found', code=status.HTTP_404_NOT_FOUND)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter()
    lookup_field = 'username'
    http_method_names = ['patch', 'get']


class RatingReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = RatingReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = RatingReview.objects.filter()

    def get_queryset(self):
        return self.queryset.filter(given_to=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            given_to = User.objects.get(username__exact=request.data.get('given_to'))
        except User.DoesNotExist:
            raise ValidationError('user not found', code=status.HTTP_404_NOT_FOUND)
        if not request.data.get('rating_value'):
            raise ValidationError('rating_value is required', code=status.HTTP_404_NOT_FOUND)
        if request.data['rating_value'] > 5 or request.data['rating_value'] < 1:
            raise ValidationError('invalid rating value', code=status.HTTP_404_NOT_FOUND)
        if given_to == self.request.user:
            raise ValidationError('user cannot rate himself', code=status.HTTP_400_BAD_REQUEST)
        try:
            settle_post = SettlePost.objects.get(created_by=self.request.user, post__slug__exact=request.data['slug'])
        except SettlePost.DoesNotExist:
            try:
                settle_post = SettlePost.objects.get(settled_with=self.request.user,
                                                     post__slug__exact=request.data['slug'])
            except SettlePost.DoesNotExist:
                raise ValidationError('post not found', code=status.HTTP_404_NOT_FOUND)
        try:
            RatingReview.objects.get(created_by=self.request.user, post=settle_post.post.id)
            raise ValidationError('review is already given', code=status.HTTP_400_BAD_REQUEST)
        except RatingReview.DoesNotExist:
            request.data['post'] = settle_post.post.id
            request.data['given_as'] = RatingReview.GivenAsOptions.MERCHANT if (
                settle_post.created_by == self.request.user
            ) else RatingReview.GivenAsOptions.BUYER
            request.data['given_to'] = given_to.id
            request.data['created_by'] = self.request.user.id
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                rating_review: RatingReview = serializer.save()
                increase_rating_value.delay(rating_review.given_to.username, rating_review.given_as)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
