from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from payment.serializers import PaymentSerializer, TransactionSerializer
from payment.models import Payment, Transaction
from payment.tasks import increase_user_balance
from payment.utils import identifier_builder
from user.models import User


class AdminPaymentListCreateAPIView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Payment.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = self.request.user.id
        request.data['method'] = Payment.PaymentMethods.ADMIN
        try:
            user = User.objects.get(username__exact=request.data.get('username'))
        except User.DoesNotExist:
            raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)
        request.data['username'] = user.username
        request.data['invoice_no'] = identifier_builder()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment: Payment = serializer.save()
            increase_user_balance.delay(invoice_no=payment.invoice_no, created_by=payment.created_by.username)
            return Response(self.get_serializer(payment).data, status=status.HTTP_201_CREATED)


class AdminTransactionListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.filter()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['username', 'post__slug']
