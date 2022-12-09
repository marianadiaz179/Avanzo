from monitoring.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def send_email(mensaje:str):
    subject = 'Estado de solicitud de crédito'
    message = mensaje
    recepient = "m.diaza2@uniandes.edu.co"
    send_mail(subject, message, EMAIL_HOST_USER, [recepient])
