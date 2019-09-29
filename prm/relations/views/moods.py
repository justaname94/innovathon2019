# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

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


class MoodsViewSet(mixins.ListModelMixin,
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
        """Check for 'from' and 'to' date query params to return a date range
           of moods. Date must be formatted as "YYYY-MM-DD" """
        # TODO: Validate date fields
        if bool('from' in request.query_params) ^ \
                bool('to' in request.query_params):
            return Response(
                {'message': 'need to add from and to date params together'},
                status=status.HTTP_400_BAD_REQUEST)
        elif 'from' in request.query_params and 'to' in request.query_params:
            queryset = Mood.objects.filter(
                owner=request.user,
                date__gte=request.query_params['from'],
                date__lte=request.query_params['to'])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
