from typing import Dict

from base.serializers import BaseModelSerializer, ReadWriteSerializerMethodField
from payment.models import Payment, Transaction
from post.serializers import PostLiteSerializer


class TransactionSerializer(BaseModelSerializer):
    post = ReadWriteSerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_post(self, instance: Transaction) -> Dict:
        if instance.post:
            return PostLiteSerializer(instance.post).data
        return {}


class PaymentSerializer(BaseModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
