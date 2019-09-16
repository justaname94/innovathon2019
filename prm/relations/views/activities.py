# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Serializers
from ..serializers import ActivityModelSerializer, AddContactSerializer

# Models
from ..models import Activity, Contact

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

    lookup_field = 'short_id'

    def get_queryset(self):
        queryset = Activity.objects.filter(owner=self.request.user)
        contact = self.request.query_params.get('contact', None)

        if contact is not None:
            queryset = queryset.filter(partners__short_id=contact)
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
            activity = get_object_or_404(Activity, **filter_kwargs)

            serializer = AddContactSerializer(
                context={
                    'activity': activity,
                    'contact': contact})
            activity = serializer.save()
            data = self.get_serializer(activity).data
            return Response(data, status.HTTP_200_OK)
        else:
            return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
            Performs a normal destroy and allows to delete an specific contact
            from an activity.
        """
        contact_id = self.request.query_params.get('contact', None)

        if contact_id is not None:
            contact = get_object_or_404(Contact, short_id=contact_id)

            filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
            activity = get_object_or_404(Activity, **filter_kwargs)

            if contact in activity.partners.all():
                activity.partners.remove(contact)
                return Response(status=status.HTTP_204_NO_CONTENT)
            # Contact does not have a relation with activity
            raise NotFound()
        else:
            return super().partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
