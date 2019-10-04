# Django
from django.db import models

# Models
from ...utils import PRMModel

# Fields
from django_extensions.db.fields import RandomCharField


class Event(PRMModel):
    """
    Represents an event from a calendar, an event is an upcoming situation
    of the user, aside from the expected information data, you can add
    which of the contacts you'll be doing it
    """

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    code = RandomCharField(length=8, blank=False, null=False, unique=True)

    description = models.CharField(max_length=2000, blank=True)

    location = models.CharField(max_length=300)

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    contacts = models.ManyToManyField('relations.Contact')
