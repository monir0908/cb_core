# Generated by Django 3.1.4 on 2022-01-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_ratingreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='buyer_rating_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='merchant_rating_value',
            field=models.FloatField(default=0),
        ),
    ]