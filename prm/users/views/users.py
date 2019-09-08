
# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from ..serializers import UserModelSerializer, UserSignUpSerializer

# Models
from ..models import User

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..permissions import IsAccountOwner


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    def get_permissions(self):
        if self.action in ['signup']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignUpSerializer
        return UserModelSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up view."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status.HTTP_200_OK)
