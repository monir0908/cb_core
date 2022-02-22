from django.urls import path

from payment.views.users import UserTransactionListAPIView

app_name = 'user.payment'

urlpatterns = [
    path('transactions', UserTransactionListAPIView.as_view(), name='user.transaction.list.api'),
]
