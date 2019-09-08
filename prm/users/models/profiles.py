# Django
from django.db import models


class Profile(models.Model):
    """Profile model"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(
        'Profile picture',
        upload_to='users/pictures',
        blank=True,
        null=True)

    address = models.CharField('Home address', max_length=250, blank=True)

    company = models.CharField(
        max_length=30, blank=True,
        help_text='Company/Organization you work or own.')

    position = models.CharField(
        max_length=50, blank=True,
        help_text='Position you hold at the company/organization you work at.')

    biography = models.TextField(blank=True)
