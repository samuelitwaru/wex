from django.core.mail import send_mail
from django.contrib.auth.models import User
from django import template
from django_q.tasks import async_task, schedule


def send_set_password_mail(email):
    password_set_email_template = template.loader.get_template(f'emails/set-password-email.html')
    user = User.objects.filter(email=email).first()
    if user:
        async_task(
            'django.core.mail.send_mail',
            'SET PASSWORD',
            "",
            'amobitinfo@gmail.com',
            [email],
            fail_silently=False,
            html_message = password_set_email_template.render({"user": user})
        )


        # send_mail(
        #     'SET PASSWORD',
        #     "",
        #     'amobitinfo@gmail.com',
        #     [email],
        #     fail_silently=False,
        #     html_message = password_set_email_template.render({"user": user})
        # )

from django.utils import timezone
from django_q.models import Schedule
from datetime import timedelta

def welcome_mail():
    msg = 'Welcome to our website'
    # send this message right away
    async_task('django.core.mail.send_mail',
            'Welcome',
            msg,
            'amobitinfo@gmail.com',
            ['samuelitwaru@gmail.com'])
    # and this follow up email in one hour
    msg = 'Here are some tips to get you started...'
    schedule('django.core.mail.send_mail',
             'Follow up',
             msg,
             'amobitinfo@gmail.com',
             ['samuelitwaru@gmail.com'],
             schedule_type=Schedule.ONCE,
             next_run=timezone.now() + timedelta(hours=3, minutes=2))
    
    send_mail(
        'SET PASSWORD',
        msg,
        'amobitinfo@gmail.com',
        ['samuelitwaru@gmail.com'],
        fail_silently=False,
        # html_message = password_set_email_template.render({"user": user})
    )