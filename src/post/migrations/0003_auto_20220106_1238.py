# Generated by Django 3.1.4 on 2022-01-06 12:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20220106_1154'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='post',
            name='posts_is_appr_c45372_idx',
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='posts_settlem_ab6d1a_idx',
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='posts_publish_8a2acf_idx',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='size',
            new_name='size_type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='post',
            name='publish_status',
        ),
        migrations.RemoveField(
            model_name='post',
            name='settlement_status',
        ),
        migrations.AddField(
            model_name='post',
            name='feature_image',
            field=models.URLField(default=datetime.datetime(2022, 1, 6, 12, 37, 50, 563959, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='live_time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='max_color_variety',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='min_color_variety',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='minimum_order_quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='size_cm_max',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='size_cm_min',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='size_inch_max',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='size_inch_min',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('published', 'published'), ('unpublished', 'unpublished'), ('drafted', 'drafted'), ('approved', 'approved'), ('waited', 'waited')], default='unpublished', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='total_interest',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='unit',
            field=models.CharField(default='pc', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='unit_price',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='unpublished_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['total_interest'], name='posts_total_i_edeb80_idx'),
        ),
    ]
