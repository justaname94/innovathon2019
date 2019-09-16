# TODO: Refactor activity and activity log serializers to unify/eliminate
# duplicate behavior

# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Activity
from ..models import Contact


class ActivityModelSerializer(serializers.ModelSerializer):
    """Mood serializer"""
    name = serializers.CharField(min_length=3)

    partners = serializers.SlugRelatedField(
        many=True,
        slug_field='first_name',
        read_only=True)

    class Meta:
        model = Activity
        exclude = ('owner', 'id', 'created', 'modified')


class AddContactToActivitySerializer(serializers.Serializer):
    contact = serializers.SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='code'
    )

    # TODO: Refactor validate contact logic for add and remove contact
    # serializers
    def validate_contact(self, contact):
        """Validate contact is not part of activity partners"""
        activity = self.context['activity']

        if contact in activity.partners.all():
            raise serializers.ValidationError(
                'Contact is alreday a member of this activity')
        return contact

    def save(self):
        activity = self.context['activity']
        contact = self.validated_data['contact']
        activity.partners.add(contact)
        return activity


class RemoveContactFromActivitySerializer(serializers.Serializer):

    contact = serializers.SlugRelatedField(
        queryset=Contact.objects.all(),
        slug_field='code'
    )

    def validate_contact(self, contact):
        """Validate contact is part of activity partners"""
        activity = self.context['activity']

        if contact not in activity.partners.all():
            raise serializers.ValidationError(
                'Contact is not a member of this activity')
        return contact

    def save(self, **kwargs):
        activity = self.context['activity']
        activity.partners.remove(self.validated_data['contact'])
        return activity
