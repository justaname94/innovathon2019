# Models
from ..models import Profile

# Django REST Framework
from rest_framework import serializers


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer"""

    class Meta:
        model = Profile
        exclude = ('user',)
