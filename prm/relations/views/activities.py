# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from ..serializers import ActivityModelSerializer

# Models
from ..models import Activity

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner


class ActivitiesViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = ActivityModelSerializer
    permission_classses = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        return Activity.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
