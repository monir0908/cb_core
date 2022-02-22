from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Avg

from user.models import User, RatingReview

logger = get_task_logger(__name__)


@shared_task(name='core.user.accumulated.rating')
def increase_rating_value(username: str, given_as: str) -> object:
    given_to = User.objects.get(username__exact=username)
    rating = RatingReview.objects.filter(given_to__username__exact=username,
                                         given_as=given_as).aggregate(Avg('rating_value'))
    if given_as == RatingReview.GivenAsOptions.BUYER:
        given_to.merchant_rating_value = round(rating.get('rating_value__avg', 0), 2)
    else:
        given_to.buyer_rating_value = round(rating.get('rating_value__avg', 0), 2)
    given_to.save()
    logger.info(f'user: {username} rating value updated')
    return
