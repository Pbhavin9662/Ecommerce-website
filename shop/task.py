from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from .models import *
from django.core.mail import EmailMultiAlternatives

@shared_task()
def sleepy(duration):  
    sleep(duration)
    return None  


@shared_task()
def send_mail_task(mail_subject,to_email,message,filename,pdf):
    email= EmailMultiAlternatives(mail_subject,
     'Hello customer',
     settings.EMAIL_HOST_USER,
    [to_email])
    email.attach_alternative(message, "text/html")
    email.attach(filename, pdf, 'application/pdf')
    email.send(fail_silently=False)
    print("----------Msg Form celery-----{{reuqest.user}}-------")
    return None


