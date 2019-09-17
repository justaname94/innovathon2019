# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

# Serializers
from ..serializers import (
    ActivityModelSerializer,
    AddContactToActivitySerializer,
    RemoveContactFromActivitySerializer)

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
    permission_classes = [IsAuthenticated, IsAccountOwner]

    lookup_field = 'code'

    def get_queryset(self):
        queryset = Activity.objects.filter(owner=self.request.user)
        contact = self.request.query_params.get('contact', None)

        if contact is not None and self.action == 'list':
            queryset = queryset.filter(partners__code=contact)
        return queryset

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
