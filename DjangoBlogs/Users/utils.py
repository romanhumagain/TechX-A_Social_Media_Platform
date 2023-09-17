from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(subject, message, to):
  email = EmailMultiAlternatives(
    subject=subject,
    body=message,
    to=[to],
    from_email=settings.EMAIL_HOST_USER,
  )
  email.content_subtype = 'html'
  email.send()
  