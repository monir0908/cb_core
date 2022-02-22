from django.db import models

from base.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class Genre(BaseModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'genres'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name
