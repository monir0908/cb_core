from django.core.management.base import BaseCommand, CommandError

from post.models import PostConfig
from user.models import User


class Command(BaseCommand):
    help = 'management command for captain banik'

    def handle(self, *args, **options):
        try:
            PostConfig.objects.get(slug__exact='pay-as-you-go-config')
            raise CommandError('post config is set')
        except PostConfig.DoesNotExist:
            try:
                user = User.objects.get(username__exact='system')
            except User.DoesNotExist:
                user = User.objects.create(
                    username='system'
                )
            PostConfig.objects.create(
                name='Pay as you go config',
                slug='pay-as-you-go-config',
                value={
                    'package_one': {
                        'live_time': 5,
                        'charge': 25,
                    },
                    'package_two': {
                        'live_time': 10,
                        'charge': 40,
                    },
                    'package_three': {
                        'live_time': 15,
                        'charge': 80,
                    },
                    'package_four': {
                        'live_time': 20,
                        'charge': 100,
                    }
                },
                created_by=user
            )
            print('pay as you go created')
            PostConfig.objects.create(
                name='Premium config',
                slug='premium-config',
                value=dict(
                    live_time=120,
                    charge=2000,
                ),
                created_by=user
            )
            print('premium created')
