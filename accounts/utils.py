from django.core.mail import EmailMessage
import os 
from decouple import config

class Util:
    @staticmethod
    def email_sender(data):
        email = EmailMessage(subject=data['subject'],body=data['body'],from_email=config('DEFAULT_FROM_EMAIL'),
                             to=[data['to_email']])
        
        email.send()
