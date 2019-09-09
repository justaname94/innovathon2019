# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Activity


class ActivityModelSerializer(serializers.ModelSerializer):
    """Mood serializer"""
    name = serializers.CharField(min_length=3)

    class Meta:
        model = Activity
        exclude = ('owner', 'created', 'modified')
