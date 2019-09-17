# Django REST Framework
from rest_framework import serializers

# Models
from ..models import ActivityLog
from ..models import Contact


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

    contact = serializers.SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='code'
    )

    # TODO: Refactor validate contact logic for add and remove contact
    # serializers on activity log
    def validate_contact(self, contact):
        """Validate contact is not part of activity companions"""
        activity_log = self.context['activity_log']

        if contact in activity_log.companions.all():
            raise serializers.ValidationError(
                'Contact is already a member of this activity log')
        return contact

    def save(self):
        activity_log = self.context['activity_log']
        contact = self.validated_data['contact']
        activity_log.companions.add(contact)
        return activity_log


class RemoveContactFromActivityLogSerializer(serializers.Serializer):

    contact = serializers.SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='code'
    )

    def validate_contact(self, contact):
        """Validate contact is part of activity companions"""
        activity_log = self.context['activity_log']

        if contact not in activity_log.companions.all():
            raise serializers.ValidationError(
                'Contact is not a member of this activity log')
        return contact

    def save(self, **kwargs):
        activity_log = self.context['activity_log']
        activity_log.companions.remove(self.validated_data['contact'])
        return activity_log
