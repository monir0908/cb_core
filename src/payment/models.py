import uuid

from django.db import models

from base.models import BaseModel


class Payment(BaseModel):
    class PaymentMethods(models.TextChoices):
        BKASH = 'bkash', 'bkash'
        NAGAD = 'nagad', 'nagad'
        ADMIN = 'admin', 'admin'

    amount = models.FloatField()
    status = models.CharField(max_length=15, choices=BaseModel.PaymentStatus.choices,
                              default=BaseModel.PaymentStatus.INIT)
    username = models.CharField(max_length=15)
    method = models.CharField(max_length=10, choices=PaymentMethods.choices)
    invoice_no = models.CharField(max_length=50, unique=True)
    transaction = models.ForeignKey('payment.Transaction', on_delete=models.SET_NULL, null=True)
    gateway_response = models.JSONField(default=dict)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return self.invoice_no


class Transaction(BaseModel):
    class Types(models.TextChoices):
        CREDIT = 'credit', 'credit'
        DEBIT = 'debit', 'debit'

    class PaymentMethods(models.TextChoices):
        BKASH = 'bkash', 'bkash'
        NAGAD = 'nagad', 'nagad'
        ADMIN = 'admin', 'admin'

    transaction_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=10, choices=Types.choices)
    username = models.CharField(max_length=15)
    amount = models.FloatField()
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT, null=True)
    method = models.CharField(max_length=10, choices=PaymentMethods.choices, default=PaymentMethods.ADMIN)

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return self.transaction_no.hex
