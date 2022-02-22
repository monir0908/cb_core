from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from payment.models import Transaction
from payment.serializers import TransactionSerializer


class UserTransactionListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['username', 'post__slug']

    def get_queryset(self):
        return Transaction.objects.filter(username__exact=self.request.user.username)
