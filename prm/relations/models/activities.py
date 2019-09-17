# Django
from django.db import models

# Models
from ...utils import PRMModel

# Fields
from django_extensions.db.fields import RandomCharField


class Activity(PRMModel):
    """
    Activity or obligation an user has, could be a hobby, responsability,
    club membership, or any other that the user belongs to.
    """

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    code = RandomCharField(length=8, blank=False, null=False, unique=True)

    name = models.CharField(max_length=50)

    description = models.TextField()

    is_active = models.BooleanField(
        "Is active",
        default=True,
        help_text="Are you currently actively doing it?")

    last_time = models.DateField('Last time done', blank=True, null=True)

    partners = models.ManyToManyField('relations.Contact')

    def __str__(self):
        return f'{self.name} by {self.owner}'
