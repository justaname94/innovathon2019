# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from ..serializers import EventModelSerializer

# Models
from ..models import Event

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING

# Mixins
from ...utils.mixins import ListModelFilterBetweenDatesMixin


class EventsViewSet(ListModelFilterBetweenDatesMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = EventModelSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    lookup_field = 'code'

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(manual_parameters=[
        Parameter('from', IN_QUERY,
                  description='Beginning date of events', type=TYPE_STRING),
        Parameter('to', IN_QUERY,
                  description='End date of events', type=TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
