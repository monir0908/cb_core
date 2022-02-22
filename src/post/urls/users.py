from django.urls import path

from post.views.users import (
    UserPostListCreateAPIView,
    UserPostRetrieveUpdateAPIView,
    UserPostInterestListCreateAPIView,
    UserPostBookListCreateAPIView,
    UserPostBookRetrieveDestroyAPIView,
    UserPostCommentListCreateApiView,
    UserPostSettleListCreateApiView,
    publish_post,
)

app_name = 'user.posts'

urlpatterns = [
    path('posts', UserPostListCreateAPIView.as_view(), name='users.post.list.create.api'),
    path('posts/<str:slug>', UserPostRetrieveUpdateAPIView.as_view(), name='users.post.get.update.api'),
    path('post-interest', UserPostInterestListCreateAPIView.as_view(), name='users.post.interest.list.create.api'),
    path('post-bookmark', UserPostBookListCreateAPIView.as_view(), name='users.post.bookmark.list.create.api'),
    path('post-bookmark/<str:slug>', UserPostBookRetrieveDestroyAPIView.as_view(),
         name='users.post.bookmark.get.delete.api'),
    path('post-comment/<str:slug>', UserPostCommentListCreateApiView.as_view(),
         name='users.post.comment.list.create.api'),
    path('post-settlement', UserPostSettleListCreateApiView.as_view(), name='users.post.settle.list.create.api'),
    path('post-publish/<str:slug>', publish_post, name='users.post.publish.create.api'),
]
