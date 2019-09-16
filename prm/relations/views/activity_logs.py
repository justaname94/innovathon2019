# TODO: Refactor activity and activity log viewsets on similar behaviors

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Serializers
from ..serializers import (
    ActivityLogModelSerializer, AddContactToActivityLogSerializer)

# Models
from ..models import Activity, ActivityLog, Contact

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

    lookup_field = 'short_id'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the activity exists"""
        act_short_id = kwargs['activity']
        self.activity = get_object_or_404(Activity, short_id=act_short_id)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ActivityLog.objects.filter(owner=self.request.user)
        contact = self.request.query_params.get('contact', None)

        if contact is not None:
            queryset = queryset.filter(companions__short_id=contact)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        """
            Performs a normal update and also allows to pass addition of
            contacts to activities via the contact param.
        """
        contact_id = self.request.query_params.get('contact', None)

        if contact_id is not None:
            contact = get_object_or_404(Contact, short_id=contact_id)

            filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
            activity_log = get_object_or_404(ActivityLog, **filter_kwargs)

            serializer = AddContactToActivityLogSerializer(
                context={
                    'activity_log': activity_log,
                    'contact': contact})
            activity_log = serializer.save()
            data = self.get_serializer(activity_log).data
            return Response(data, status.HTTP_200_OK)
        else:
            return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
            Performs a normal destroy and allows to delete an specific contact
            from an activity log.
        """
        contact_id = self.request.query_params.get('contact', None)

        if contact_id is not None:
            contact = get_object_or_404(Contact, short_id=contact_id)

            filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
            activity_log = get_object_or_404(ActivityLog, **filter_kwargs)

            if contact in activity_log.companions.all():
                activity_log.companions.remove(contact)
                return Response(status=status.HTTP_204_NO_CONTENT)
            # Contact does not have a relation with activity log
            raise NotFound()
        else:
            return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, activity=self.activity)
