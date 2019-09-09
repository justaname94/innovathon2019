# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Only allow users to interact with their own data"""

    def has_object_permission(self, request, view, obj):
        """Check if the authenticated user is the same as the request user."""
        return request.user == obj
