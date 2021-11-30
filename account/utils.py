from celery import shared_task
from django.core.mail import send_mail
from logram.celery import app

from django.core.mail import send_mail


@app.task
def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""Thank you for registration. Activate your account here:
    http://127.0.0.1:8000/api/v1/account/activation/{activation_code}"""

    send_mail('Account activation',message,'test@logram.com', [email, ], fail_silently=False, )

@app.task
def send_activation_mail(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""To reset your password click here {activation_url}"""

    send_mail('Password reset',message,'test@logram.com', [email, ], fail_silently=False, )
