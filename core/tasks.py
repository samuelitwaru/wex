from django.core.mail import send_mail
from wex.celery import app
from celery import shared_task
from django import template
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives

@shared_task
def send_welcome_mail(host, username, token_key):
    user = User.objects.filter(username=username).first()
    if user:
        ctx = {"host": host, "user": user, "token_key": token_key}
        html =  template.loader.get_template('emails/welcome-mail.html').render(ctx)        
        send_mail(
            'WELCOME',
            'msg',
            'amobitinfo@gmail.com',
            [user.email],
            fail_silently=False,
            html_message = html
        )