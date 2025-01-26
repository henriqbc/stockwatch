from django.shortcuts import render
from django.core.mail import EmailMessage, send_mail
from stockwatch.settings import EMAIL_HOST_USER

def send_email(request):
    pass