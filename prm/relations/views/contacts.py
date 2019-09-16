# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from ..serializers import ContactModelSerializer

# Models
from ..models import Contact

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner


class ContactsViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = ContactModelSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    lookup_field = 'short_id'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
