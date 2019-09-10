"""Django models utilities"""

# Django
from django.db import models


class PRMModel(models.Model):
    """PRM base model.

    PRMMModel acts as an abstract base class from which every other model
    in the project will inherit. This class provides every table with the
    following attributes:
        + created(Datetime): Store the datetime the object was created.
        + modified(Datetime): Store the last datetime the object was modified.
    """
    created = models.DateTimeField(
        'created at ',
        auto_now_add=True,
        help_text='Datetime on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified at ',
        auto_now=True,
        help_text='Datetime on which the object was last modified.'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']


class Entity(PRMModel):
    """Entity Base model

    Entity acts as a base class that holds personal information of a live
    being, it is provided as a way of unifying all the personal data a living
    entity might have.
    """

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

    birth_date = models.DateField('Birth Date', blank=True, null=True)

    class Meta(PRMModel.Meta):
        abstract = True
