
# Django
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model, featuring email sign in"""

    email = models.EmailField(
        'Email address',
        unique=True,
        error_messages={
            'unique': 'An user with this email already exists'
        })

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Phone number must be entered in the format: +999999999. Up '
                 'to 15 digits allowed.')
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        get_latest_by = ('date_joined',)
