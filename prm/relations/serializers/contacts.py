# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Contact


class ContactModelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Contact
        exclude = ('created', 'modified')
        read_only_fields = ('id',)
