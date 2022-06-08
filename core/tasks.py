from django.core.mail import send_mail
from wex.celery import app
from celery import shared_task
from django import template
from django.contrib.auth.models import User


@shared_task
def send_welcome_mail(username):
    user = User.objects.filter(username=username).first()
    if user:
        welcome_mail_template = template.loader.get_template(f'emails/welcome-mail.html')
        msg = 'Welcome to our website'
        send_mail(
            'WELCOME',
            msg,
            'amobitinfo@gmail.com',
            [user.email],
            fail_silently=False,
            html_message = welcome_mail_template.render({"user": user})
        )