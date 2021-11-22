from celery import shared_task
from time import sleep


@shared_task
def simple_task(x: int, y: int):
    sleep(1)
    return x + y
