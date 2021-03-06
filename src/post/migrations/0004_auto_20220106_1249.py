# Generated by Django 3.1.4 on 2022-01-06 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_auto_20220106_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('settlement_date', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_settleposts', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.post')),
                ('settled_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post_settled_by', to=settings.AUTH_USER_MODEL)),
                ('settled_with', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post_settled_with', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_settleposts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post_settlement',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_postsizes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.post')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_postsizes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post_sizes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_postcomments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.post')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_postcomments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post_comments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='settlepost',
            index=models.Index(fields=['-created_at'], name='post_settle_created_da741c_idx'),
        ),
        migrations.AddIndex(
            model_name='settlepost',
            index=models.Index(fields=['settlement_date'], name='post_settle_settlem_be994e_idx'),
        ),
        migrations.AddIndex(
            model_name='postsize',
            index=models.Index(fields=['-created_at'], name='post_sizes_created_61011a_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['-created_at'], name='post_commen_created_76134c_idx'),
        ),
    ]
