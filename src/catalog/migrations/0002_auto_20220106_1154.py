# Generated by Django 3.1.4 on 2022-01-06 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_genres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='genre',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_genres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_categorys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_categorys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='genres_name_4778a7_idx'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['-created_at'], name='genres_created_a1b277_idx'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['is_active'], name='genres_is_acti_9fc31c_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='categories_name_98d7d5_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['-created_at'], name='categories_created_9211a1_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['is_active'], name='categories_is_acti_aae090_idx'),
        ),
    ]
