from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import F

from payment.models import Payment, Transaction
from user.models import User
from post.models import Post

logger = get_task_logger(__name__)


@shared_task(name='core.payment.increment.balance')
def increase_user_balance(invoice_no: str, created_by: str) -> object:
    payment = Payment.objects.get(invoice_no__exact=invoice_no)
    user = User.objects.get(username__exact=payment.username)
    with transaction.atomic():
        user.balance = F('balance') + payment.amount
        user.save()
        logger.info('user balance has been updated')
        t = Transaction.objects.create(
            type=Transaction.Types.CREDIT,
            username=user.username,
            amount=payment.amount,
            created_by=User.objects.get(username__exact=created_by)
        )
        logger.info('transaction created for user')
        payment.transaction = t
        payment.save()
        logger.info('payment updated for user')
    logger.info('transaction creating job done!!')
    return


@shared_task(name='core.payment.decrement.balance')
def decrease_user_balance(updated_by: str, post_slug: str) -> object:
    post = Post.objects.get(slug__exact=post_slug)
    user = User.objects.get(username__exact=updated_by)
    with transaction.atomic():
        user.balance = F('balance') - post.points_needed
        user.save()
        logger.info('user balance has decreased')
        Transaction.objects.create(
            type=Transaction.Types.DEBIT,
            username=post.username,
            amount=post.points_needed,
            created_by=User.objects.get(username__exact=user),
            post=post,
        )
        logger.info('transaction created for user')
    logger.info('transaction creating job done!!')
    return
