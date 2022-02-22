from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        ARCHIVED = 'archived', _('archived')

    class PaymentStatus(models.TextChoices):
        INIT = 'init', 'init'
        SUCCESS = 'success', 'success',
        FAILED = 'failed', 'failed'
        CANCELED = 'canceled', 'canceled'

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='created_%(class)ss')
    updated_by = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='updated_%(class)ss', null=True,
                                   blank=True)

    class Meta:
        abstract = True
        app_label = 'base'
