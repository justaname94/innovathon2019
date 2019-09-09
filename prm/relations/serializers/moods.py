# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Mood

# Utils
from django.utils import timezone
from datetime import date


class MoodModelSerializer(serializers.ModelSerializer):
    """Mood serializer"""

    class Meta:
        model = Mood
        exclude = ('owner', 'id', 'created', 'modified')

    def validate_date(self, data):
        """Validate that can only set moods in the past"""
        now = timezone.now()
        today = date(year=now.year, month=now.month, day=now.day)
        if (data > today):
            raise serializers.ValidationError(
                'Can only log moods from today or the past')
        return data
