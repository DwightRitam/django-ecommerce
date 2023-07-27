

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage


def send_account_activation(email,email_token,email_Otp):
    subject = 'Your account has to be activate.'
    
    message = f'Hey user, Welcome to FilmoTrend here is your otp {email_Otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,{email})