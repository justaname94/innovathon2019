
# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from ..serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    UserVerificationSerializer,
    UserLoginSerializer,
    UserModelTokenSerializer,
    ProfileModelSerializer
)

# Models
from ..models import User, Profile

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..permissions import IsAccountOwner

# Swagger
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi


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

    @swagger_auto_schema(
        security=[],
        request_body=UserSignUpSerializer,
        responses={
            status.HTTP_201_CREATED: UserModelSerializer
        })
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up view, after successful registration, an email is sent
           to the user with a verification token that expires on 3 days."""
        serializer = UserSignUpSerializer(data=request.data, context={
            'request': request
        })
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status.HTTP_201_CREATED)

    # Next time I'll manually write the api documentation because
    # this is absurd
    @swagger_auto_schema(
        security=[],
        manual_parameters=[openapi.Parameter(
            'token', openapi.IN_QUERY,
            description="Verification token sent to user",
            type=openapi.TYPE_STRING)],
        request_body=no_body,
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'message': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Success message')},
        )})
    @action(detail=False, methods=['get'])
    def verify(self, request):
        """User verification by jwt token view."""
        token = self.request.query_params.get('token', None)

        if token is None:
            return Response({'token': 'Missing query parameter: token'},
                            status.HTTP_400_BAD_REQUEST)

        serializer = UserVerificationSerializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'You have been sucessfully verified'}
        return Response(data, status.HTTP_200_OK)

    @swagger_auto_schema(security=[], request_body=UserLoginSerializer,
                         responses={
                             status.HTTP_200_OK: UserModelTokenSerializer})
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login endpoint, returns user's info and authorization token"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        user.token = token
        data = UserModelTokenSerializer(user).data
        return Response(data, status.HTTP_200_OK)

    @swagger_auto_schema(method='get', responses={
        status.HTTP_200_OK: UserModelSerializer})
    @swagger_auto_schema(
        methods=['put', 'patch'],
        request_body=ProfileModelSerializer,
        responses={
            status.HTTP_200_OK: ProfileModelSerializer})
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Performs actions only on profile fields"""
        print(request.method)
        if request.method == 'GET':
            data = UserModelSerializer(self.request.user).data

            return Response(data, status.HTTP_200_OK)
        elif request.method == 'PATCH' or request.method == 'PUT':
            profile = Profile.objects.get(user=self.request.user)
            serializer = ProfileModelSerializer(
                profile,
                data=request.data,
                partial=request.method == 'PUT')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
