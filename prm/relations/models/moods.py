# Django
from django.db import models

# Models
from ...utils import PRMModel


class Mood(PRMModel):
    """
    User feeling or mood during a day, serve as a log on how the user
    have been feeling lately.
    """

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    HAPPY = 5
    GOOD = 4
    NEUTRAL = 3
    BAD = 2
    SAD = 1
    MOOD_CHOICES = (
        (HAPPY, 'happy'),
        (GOOD, 'good'),
        (NEUTRAL, 'neutral'),
        (BAD, 'bad'),
        (SAD, 'sad')
    )
    hightlights = models.CharField(max_length=200)
    mood = models.SmallIntegerField(choices=MOOD_CHOICES)
    description = models.TextField()
    date = models.DateField()

    class Meta:
        ordering = ['date', ]
        get_latest_by = 'date'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Assures that saving to an existing date will overwrite the data"""
        date = self.date
        try:
            existing_mood = Mood.objects.get(date=date)
            if self != existing_mood:
                existing_mood.description = self.description
                existing_mood.mood = self.mood
                return existing_mood.save()
        except Mood.DoesNotExist:
            pass
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
