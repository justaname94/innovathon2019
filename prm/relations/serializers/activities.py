# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Activity


class ActivityModelSerializer(serializers.ModelSerializer):
    """Mood serializer"""
    name = serializers.CharField(min_length=3)

    partners = serializers.SlugRelatedField(
        many=True,
        slug_field='first_name',
        read_only=True)

    class Meta:
        model = Activity
        exclude = ('owner', 'created', 'modified')


class AddContactSerializer(serializers.Serializer):

    """
    This serializer is purposely left empty in case additional custom validation
    and/or fields need to be added.
    """

    def save(self):
        activity = self.context['activity']
        contact = self.context['contact']
        activity.partners.add(contact)
        return activity
