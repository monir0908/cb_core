from django.urls import path

from post.views.admin import (
    AdminPostRetrieveUpdateAPIView,
    AdminPostListAPIView,
    AdminPostConfigListAPIView,
    AdminPostConfigRetrieveUpdateAPIView,
    approve_post
)

app_name = 'admin.post'

urlpatterns = [
    path('posts', AdminPostListAPIView.as_view(), name='admin.post.list.api'),
    path('posts/<str:slug>', AdminPostRetrieveUpdateAPIView.as_view(), name='admin.post.update.api'),
    path('post-approve/<str:slug>', approve_post, name='admin.post.approve.api'),
    path('post-configs', AdminPostConfigListAPIView.as_view(), name='admin.post.config.api'),
    path('post-configs/<str:slug>', AdminPostConfigRetrieveUpdateAPIView.as_view(), name='admin.post.config.get.api'),
]
