from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_mail_async(data):
    send_mail(**data)
    return True
