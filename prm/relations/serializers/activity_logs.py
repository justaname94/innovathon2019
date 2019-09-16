# Django REST Framework
from rest_framework import serializers

# Models
from ..models import ActivityLog


class ActivityLogModelSerializer(serializers.ModelSerializer):
    """Mood serializer"""

    companions = serializers.SlugRelatedField(
        many=True,
        slug_field='first_name',
        read_only=True)

    activity = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ActivityLog
        exclude = ('owner', 'id', 'created', 'modified')


class AddContactToActivityLogSerializer(serializers.Serializer):

    """
    This serializer is purposely left empty in case additional custom validation
    and/or fields need to be added.
    """

    def save(self):
        activity_log = self.context['activity_log']
        contact = self.context['contact']
        activity_log.companions.add(contact)
        return activity_log
