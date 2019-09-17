# TODO: Refactor activity and activity log viewsets on similar behaviors

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

# Serializers
from ..serializers import (
    ActivityLogModelSerializer,
    AddContactToActivityLogSerializer,
    RemoveContactFromActivityLogSerializer)

# Models
from ..models import Activity, ActivityLog

# Permissions
from rest_framework.permissions import IsAuthenticated
from prm.users.permissions import IsAccountOwner


class ActivitiyLogsViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    serializer_class = ActivityLogModelSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    lookup_field = 'code'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the activity exists"""
        activity_code = kwargs['activity']
        self.activity = get_object_or_404(Activity, code=activity_code)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ActivityLog.objects.filter(owner=self.request.user)
        contact = self.request.query_params.get('contact', None)

        if contact is not None and self.action == 'list':
            queryset = queryset.filter(companions__code=contact)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        """
            Performs a normal update and also allows to pass addition of
            contacts to activities via the contact param.
        """
        contact_code = self.request.query_params.get('contact', None)

        if contact_code is None:
            return super().partial_update(request, *args, **kwargs)

        # This is so the get queryset doesn't filter by contact
        activity_log = self.get_object()
        serializer = AddContactToActivityLogSerializer(
            data={'contact': contact_code},
            context={'activity_log': activity_log, })
        serializer.is_valid(raise_exception=True)
        activity_log = serializer.save()

        data = self.get_serializer(activity_log).data
        return Response(data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
            Performs a normal destroy and allows to delete an specific contact
            from an activity log.
        """
        contact_code = self.request.query_params.get('contact', None)

        if contact_code is None:
            return super().destroy(request, *args, **kwargs)

        activity_log = self.get_object()
        serializer = RemoveContactFromActivityLogSerializer(
            data={'contact': contact_code},
            context={'activity_log': activity_log}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, activity=self.activity)
