from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('admin/', include('user.urls.admin', namespace='admin.user.views')),
    path('users/', include('user.urls.users', namespace='users.user.views')),
]
