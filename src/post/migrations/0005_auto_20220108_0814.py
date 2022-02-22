# Generated by Django 3.1.4 on 2022-01-08 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20220106_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='color',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('published', 'published'), ('unpublished', 'unpublished'), ('drafted', 'drafted'), ('approved', 'approved'), ('waited', 'waited'), ('settled', 'settled')], max_length=30),
        ),
    ]
