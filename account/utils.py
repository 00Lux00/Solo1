from celery import shared_task
from django.core.mail import send_mail
from logram.celery import app

from django.core.mail import send_mail


@app.task
def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""Thank you for registration. Activation code:
    {activation_url}"""

    send_mail('Account activation',message,'andrejbotinkov@gmail.com', [email, ], fail_silently=False, )

@app.task
def send_activation_mail(user):
    activation_url = f'{user.activation_code}'
    message = f"""To reset your password click here {activation_url}"""
    email=user.email
    send_mail('Password reset',message,'andrejbotinkov@gmail.com', [email, ], fail_silently=False, )
