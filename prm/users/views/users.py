
# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from ..serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    UserVerificationSerializer,
    UserLoginSerializer
)

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

    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup', 'verify', 'login']:
            permissions = [AllowAny]
        elif self.action in [
                'retrieve', 'update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            # Method not allowed
            return []
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up view."""
        serializer = UserSignUpSerializer(data=request.data, context={
            'request': request
        })
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """User verification by jwt token view."""
        serializer = UserVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'You have been sucessfully verified'}
        return Response(data, status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Same as the retrieve, but does not require an id"""
        data = {
            'user': UserModelSerializer(self.request.user).data,
        }
        return Response(data, status.HTTP_200_OK)
