# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Event


class EventModelSerializer(serializers.ModelSerializer):
    """Event serializer"""

    contacts = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        read_only=True)

    class Meta:
        model = Event
        exclude = ('owner', 'id', 'created', 'modified')

    def validate_start_time(self, data):
        """Discard seconds from time, leaving only hour and minutes"""
        data = data.strftime("%H:%M")
        return data

    def validate_end_time(self, data):
        """Discard seconds from time, leaving only hour and minutes"""
        data = data.strftime("%H:%M")
        return data
