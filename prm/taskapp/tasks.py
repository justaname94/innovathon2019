"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Django REST Framework
from rest_framework.reverse import reverse

# Models
from ..users.models import User

# Celery
from celery import task

# Utils
from django.utils import timezone
from datetime import timedelta

# JWT
import jwt


def gen_verification_token(user):
    """Generate JWT necessary for the user to authenticate its account"""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': exp_date,
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk, host):
    user = User.objects.get(pk=user_pk)
    token = gen_verification_token(user)
    subject = 'Verify your email at Personal CRM (PRM)'
    from_email = 'Personal CRM <noreply@prm.com>'
    html_content = render_to_string('emails/users/register_confirmation.html', {
        'user': user,
        'token': token,
        'type': 'email_confirmation',
        'verification_link': f"{host}{reverse('users:users-verify')}"
    })
    text_content = strip_tags(html_content)

    message = EmailMultiAlternatives(
        subject, text_content, from_email, [user.email])
    message.attach_alternative(html_content, 'text/html')
    message.send()
