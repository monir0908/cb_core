# Generated by Django 3.1.4 on 2022-01-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20220110_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='identifier',
            field=models.CharField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]