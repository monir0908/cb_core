from django.urls import path, include

app_name = 'category'

urlpatterns = [
    path('admin/', include('catalog.urls.admin', namespace='admin.catalog.views')),
    path('users/', include('catalog.urls.users', namespace='users.catalog.views')),
    path('public/', include('catalog.urls.public', namespace='public.catalog.views')),
]
