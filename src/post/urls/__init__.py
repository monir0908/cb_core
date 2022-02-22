from django.urls import path, include

app_name = 'category'

urlpatterns = [
    path('admin/', include('post.urls.admin', namespace='admin.post.views')),
    path('users/', include('post.urls.users', namespace='users.post.views')),
]
