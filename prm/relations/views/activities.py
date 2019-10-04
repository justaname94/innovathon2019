# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Serializers
from ..serializers import (
    ActivityModelSerializer,
    AddContactToActivitySerializer,
    RemoveContactFromActivitySerializer,
    ActivityLogModelSerializer)

# Models
from ..models import Activity, ActivityLog

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING


class ActivitiesViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = ActivityModelSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    lookup_field = 'code'

    def get_queryset(self):
        queryset = Activity.objects.filter(owner=self.request.user)
        contact = self.request.query_params.get('contact', None)

        if contact is not None and self.action == 'list':
            queryset = queryset.filter(partners__code=contact)
        return queryset

    @swagger_auto_schema(manual_parameters=[
        Parameter('contact', IN_QUERY,
                  description=(
                      '(Optional) contact code. If present, will add '
                      'the contact to the activities partners'),
                  type=TYPE_STRING),
    ])
    def partial_update(self, request, *args, **kwargs):
        """
            Performs a normal update and also allows to pass addition of
            contacts to activities via the contact param.
        """

        contact_code = self.request.query_params.get('contact', None)

        if contact_code is None:
            return super().partial_update(request, *args, **kwargs)

        activity = self.get_object()
        serializer = AddContactToActivitySerializer(
            data={'contact': contact_code, },
            context={'activity': activity, })
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        data = self.get_serializer(activity).data
        return Response(data, status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[
        Parameter('contact', IN_QUERY,
                  description=(
                      '(Optional) contact code. If present, will delete '
                      'the contact to the activities partners'),
                  type=TYPE_STRING),
    ])
    def destroy(self, request, *args, **kwargs):
        """
            Performs a normal destroy and allows to delete an specific contact
            from an activity.
        """
        contact_code = self.request.query_params.get('contact', None)

        if contact_code is None:
            return super().destroy(request, *args, **kwargs)

        activity = self.get_object()
        serializer = RemoveContactFromActivitySerializer(
            data={'contact': contact_code},
            context={'activity': activity}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(method='get', responses={
        status.HTTP_200_OK: ActivityLogModelSerializer})
    @action(detail=False, methods=['get'])
    def logs(self, request):
        """Returns all logs from all activities"""
        queryset = ActivityLog.objects.filter(
            owner=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActivityLogModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ActivityLogModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
