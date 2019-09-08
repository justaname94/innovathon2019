# Models
from ..models import User

# Serializers
from ..serializers import ProfileModelSerializer

# Django REST Framework
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    """User serializer"""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
            'phone_number',
            'birth_date',
        )
