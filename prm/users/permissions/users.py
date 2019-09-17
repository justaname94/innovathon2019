# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from ..models import User


class IsAccountOwner(BasePermission):
    """Only allow users to interact with their own data"""

    def has_object_permission(self, request, view, obj):
        """Check if the authenticated user is the same as the request user. Also
         works for other objects if their account property is called 'owner'.
        """
        if (isinstance(obj, User)):
            return request.user == obj
        if hasattr(obj, 'owner'):
            return request.user == obj.owner
        return False
