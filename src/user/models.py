from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin):
    verified = models.BooleanField(default=True)
    profile_pic_url = models.TextField(null=True)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True, )
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    should_send_email = models.BooleanField(default=False)
    buyer_rating_value = models.FloatField(default=0)
    merchant_rating_value = models.FloatField(default=0)
    settled_post = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    balance = models.FloatField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_superuser', 'is_staff', 'is_active', 'first_name', 'last_name']
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['-username']
        default_permissions = ('add', 'change', 'view', )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.PROTECT)
    company_name = models.CharField(max_length=100)
    company_image = models.URLField(null=True)
    address = models.TextField()
    bin = ArrayField(models.URLField(), default=list, size=5)
    bin_no = models.CharField(null=True, max_length=50)
    tin = ArrayField(models.URLField(), default=list, size=5)
    tin_no = models.CharField(null=True, max_length=50)
    trade_licence = ArrayField(models.URLField(), default=list)
    trade_licence_no = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'user_profiles'
        verbose_name_plural = 'User Profiles'
        verbose_name = 'User Profiles'

    def __str__(self):
        return self.user.username


class RatingReview(BaseModel):
    class GivenAsOptions(models.TextChoices):
        MERCHANT = 'merchant', 'merchant'
        BUYER = 'buyer', 'buyer'

    given_to = models.ForeignKey('user.User', on_delete=models.PROTECT)
    given_as = models.CharField(max_length=10, choices=GivenAsOptions.choices)
    rating_value = models.IntegerField()
    review = models.TextField()
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)

    class Meta:
        db_table = 'rating_reviews'

    def __str__(self):
        return self.given_to.username


class PremiumUser(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.PROTECT)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    premium_fee = models.FloatField()

    class Meta:
        db_table = 'premium_users'

    def __str__(self):
        return self.user.username




