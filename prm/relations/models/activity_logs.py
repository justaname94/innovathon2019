from ...utils import PRMModel
from django.db import models
from django_extensions.db.fields import RandomCharField


class ActivityLog(PRMModel):
    """
    An activity log is a moment in which you performed the activity, you can
    then add specific info of what you did and with who you did it. For example
    an activity could be biking an a log would be a day you went biking.
    """

    code = RandomCharField(length=8, blank=False, null=False, unique=True)

    activity = models.ForeignKey(
        'relations.Activity', on_delete=models.SET_NULL, null=True)

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    companions = models.ManyToManyField(
        'relations.Contact',
        help_text='Contacts with who you did the activity')

    details = models.TextField()

    date = models.DateField()

    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.activity.name} on {self.date} by {self.owner}'
