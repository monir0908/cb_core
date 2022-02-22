import random
from typing import Tuple

from django.db import connection
from rest_framework import status
from rest_framework.exceptions import ValidationError

from post.models import PostConfig


def identifier_builder() -> str:
    with connection.cursor() as cur:
        cur.execute('''SELECT last_value FROM posts_id_seq;''')
        row = cur.fetchone()
    seq_id = str(row[0] + 1)
    random_suffix = random.randint(10, 99)
    return 'CB' + seq_id.rjust(8, '0') + str(random_suffix)


def get_pay_as_you_go_config(package: str) -> Tuple[int, float]:
    try:
        post_config = PostConfig.objects.get(slug__exact='pay-as-you-go-config')
        if not post_config.value.get(package):
            raise ValidationError('invalid package selected', code=status.HTTP_404_NOT_FOUND)
        return post_config.value[package]['live_time'], post_config.value[package]['charge']
    except PostConfig.DoesNotExist:
        raise ValidationError('config not found', code=status.HTTP_404_NOT_FOUND)


def get_premium_config() -> int:
    try:
        post_config = PostConfig.objects.get(slug__exact='premium-config')
        return post_config.value['live_time']
    except PostConfig.DoesNotExist:
        raise ValidationError('config not found', code=status.HTTP_404_NOT_FOUND)

