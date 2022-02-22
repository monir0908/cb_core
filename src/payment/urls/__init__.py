from django.urls import path, include

app_name = 'payment'

urlpatterns = [
    path('admin/', include('payment.urls.admin', namespace='admin.payment.views')),
    path('users/', include('payment.urls.users', namespace='users.payment.views')),
]
