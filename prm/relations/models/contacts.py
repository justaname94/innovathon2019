# Django
from django.db import models
from django.core.validators import RegexValidator

# Models
from ...utils import Entity

# Fields
from django_extensions.db.fields import RandomCharField


class Contact(Entity):
    """Represents a contact of an user and holds all the personal
       information related to them."""

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='User this contact belongs')

    code = RandomCharField(length=8, blank=False, null=False, unique=True)

    first_name = models.CharField('First name', max_length=40)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=40)

    email = models.EmailField(blank=True)

    nickname = models.CharField(
        max_length=40,
        blank=True,
        help_text="Nickname for what they're commonly known, if they have")

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

    met = models.TextField(
        'How you met',
        blank=True,
        help_text=(
            'Describe how you met the contact, like'
            'at tahe park or at a party'))

    food_preferences = models.TextField(
        'Food preferences',
        blank=True,
        help_text='Food preferences, quirks or allergies of the contact')

    pets = models.TextField(
        "Pets",
        blank=True,
        help_text='Pets information, as their name, breed, etc..')

    def __str__(self):
        return f'{self.first_name} {self.last_name} of {self.owner}'
