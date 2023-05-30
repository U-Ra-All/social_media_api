import time

from celery import shared_task


@shared_task
def publish_post(post, delay):
    time.sleep(delay)
    post.save()
