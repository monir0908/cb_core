from celery import shared_task
from celery.utils.log import get_task_logger

from post.models import Post
from user.models import User

logger = get_task_logger(__name__)


@shared_task(name='core.posts.increment.interest')
def increase_interest_count(slug: str) -> object:
    post = Post.objects.get(slug__exact=slug)
    post.total_interest += 1
    post.save()
    logger.info(f'post: {slug} interest increased')
    return


@shared_task(name='core.posts.increment.settled.post')
def increase_settlement_count(username: str, post_id: int) -> object:
    user = User.objects.get(username__exact=username)
    user.settled_post += 1
    user.save()
    logger.info(f'user: {username} settle post count increased')
    post = Post.objects.get(pk=post_id)
    post.status = Post.Statuses.SETTLED
    post.save()
    return
