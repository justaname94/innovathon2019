# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from ..serializers import MoodModelSerializer

# Models
from ..models import Mood

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING

# Mixins
from ...utils.mixins import ListModelFilterBetweenDatesMixin


class MoodsViewSet(ListModelFilterBetweenDatesMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    lookup_field = 'date'

    serializer_class = MoodModelSerializer
    permission_classses = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        return Mood.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(manual_parameters=[
        Parameter('from', IN_QUERY,
                  description='Beginning date of moods', type=TYPE_STRING),
        Parameter('to', IN_QUERY,
                  description='End date of moods', type=TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
