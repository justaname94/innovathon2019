# Django
from django.db import models

# Models
from ...utils.models import Entity


class Profile(Entity):
    """Profile model"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        get_latest_by = ('created',)
