"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title='Captain Banik Core Service',
        default_version='v1.0',
        description="Captain banik core api service for posting showing interest etc.",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)

)

v3_patterns = [
    path('catalog/', include('catalog.urls', namespace='catalog.apis')),
    path('user-module/', include('user.urls', namespace='core.apis')),
    path('core/', include('post.urls', namespace='post.apis')),
    path('payment/', include('payment.urls', namespace='payment.apis')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check),
    path('api/', include([
        path('v1.0/', include(v3_patterns))
    ])),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
