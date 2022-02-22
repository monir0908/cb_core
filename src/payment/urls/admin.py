from django.urls import path

from payment.views.admin import AdminPaymentListCreateAPIView, AdminTransactionListAPIView

app_name = 'admin.payment'

urlpatterns = [
    path('payments', AdminPaymentListCreateAPIView.as_view(), name='admin.payment.list.api'),
    path('transactions', AdminTransactionListAPIView.as_view(), name='admin.transaction.list.api'),
]
