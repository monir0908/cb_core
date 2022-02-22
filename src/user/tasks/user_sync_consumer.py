from typing import Dict

from celery import bootsteps
from celery.utils.log import get_task_logger
from kombu import Consumer, Exchange, Queue

from core.settings import celery_app
from user.models import User

logger = get_task_logger(__name__)

AUTH_USER_SYNC_QUEUE = 'auth.events.user.sync.core'

exchange = Exchange('auth.fanout.exchange', type='fanout')

user_sync_queue = Queue(name=AUTH_USER_SYNC_QUEUE,
                        exchange=exchange, routing_key=AUTH_USER_SYNC_QUEUE)


class UserSyncConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[user_sync_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    @staticmethod
    @celery_app.task(name=AUTH_USER_SYNC_QUEUE)
    def handle_message(body, message):
        if body.get('user'):
            sync_user(body.get('user'))
        else:
            logger.info('user info with null value provided')
        message.ack()


def sync_user(data: Dict) -> object:
    try:
        user = User.objects.get(username__exact=data.get('username'))
        logger.info(f'user found with given username: {data["username"]}')
    except User.DoesNotExist:
        logger.info(f'creating new user with username: {data["username"]}')
        user = User()
        user.username = data.get('username')
    try:
        user.verified = data.get('is_verified')
        user.profile_pic_url = data.get('profile_pic_url')
        user.email = data.get('email')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.is_active = data.get('is_active', True)
        user.is_staff = data.get('is_staff', False)
        user.is_superuser = data.get('is_superuser', False)
        user.save()
        logger.info(f'user update or create task done for {data["username"]}')
    except Exception as err:
        logger.error(f'user cannot be updated or created {data["username"]}. reason: {err}')
    return


celery_app.steps['consumer'].add(UserSyncConsumer)
