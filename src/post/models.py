from email.policy import default

from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import BaseModel


class Post(BaseModel):
    class Statuses(models.TextChoices):
        PUBLISHED = 'published', 'published'
        UNPUBLISHED = 'unpublished', 'unpublished'
        DRAFTED = 'drafted', 'drafted'
        APPROVED = 'approved', 'approved'
        WAITED = 'waited', 'waited'
        SETTLED = 'settled', 'settled'

    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    identifier = models.CharField(max_length=40, unique=True, blank=False, null=False)
    live_time = models.IntegerField()
    images = ArrayField(models.URLField(), size=5)
    feature_image = models.URLField()
    description = models.TextField(max_length=150)
    quantity = models.PositiveIntegerField()
    size_type = models.CharField(max_length=20)
    size_inch_max = models.FloatField(null=True)
    size_inch_min = models.FloatField(null=True)
    size_cm_max = models.FloatField(null=True)
    size_cm_min = models.FloatField(null=True)
    status = models.CharField(max_length=30, choices=Statuses.choices)
    genre = models.ForeignKey(to='catalog.Genre', on_delete=models.PROTECT)
    category = models.ForeignKey(to='catalog.Category', on_delete=models.PROTECT)
    unit = models.CharField(max_length=15)
    unit_price = models.FloatField()
    minimum_order_quantity = models.IntegerField(null=True)
    min_color_variety = models.IntegerField(null=True)
    max_color_variety = models.IntegerField(null=True)
    meta = models.JSONField(default=dict)
    points_needed = models.PositiveIntegerField(null=True)
    username = models.CharField(max_length=20)
    published_at = models.DateTimeField(null=True)
    unpublished_at = models.DateTimeField(null=True)
    total_interest = models.IntegerField(default=0)
    send_notification = models.BooleanField(default=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['total_interest']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.title


class PostInterest(BaseModel):
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    meta = models.JSONField(default=dict)

    class Meta:
        db_table = 'post_interests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.post.title


class PostBookmark(BaseModel):
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'post_bookmarks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.post.title


class PostSize(BaseModel):
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)
    value = models.CharField(max_length=20)

    class Meta:
        db_table = 'post_sizes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.post.title


class PostComment(BaseModel):
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)
    comment = models.TextField(null=False)

    class Meta:
        db_table = 'post_comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.post.title


class SettlePost(BaseModel):
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT)
    settled_with = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='post_settled_with')
    settlement_date = models.DateField()

    class Meta:
        db_table = 'post_settlement'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['settlement_date']),
        ]

    def __str__(self):
        return self.post.title


class PostConfig(BaseModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=False, blank=False, max_length=160)
    value = models.JSONField(default=dict)

    class Meta:
        db_table = 'post_configs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

