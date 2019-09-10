# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string

# Models
from ..models import User
from ..models import Profile
from rest_framework.authtoken.models import Token

# Serializers
from .profiles import ProfileModelSerializer

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Utils
from django.utils import timezone
from datetime import timedelta

# JWT
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User serializer, can also update the profile info related to the user"""

    profile = ProfileModelSerializer()

    class Meta:
        model = User
        fields = (
            'profile',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
        )

    def update(self, instance, data):
        # Update profile info
        profile_serializer = self.fields['profile']
        profile = instance.profile
        profile_data = data.pop('profile')
        profile_serializer.update(profile, profile_data)

        return super().update(instance, data)


class UserSignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField(min_length=2, max_length=60)
    last_name = serializers.CharField(min_length=2, max_length=80)

    email = serializers.EmailField(validators=[
        UniqueValidator(User.objects.all())])

    username = serializers.CharField(
        min_length=3,
        max_length=30,
        validators=[UniqueValidator(User.objects.all())])

    birth_date = serializers.DateField(required=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Phone number must be entered in the format: +999999999. Up '
                 'to 15 digits allowed.')
    )

    phone_number = serializers.CharField(
        validators=[phone_regex], required=False)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate password match"""
        password = data['password']
        password_conf = data['password_confirmation']
        if password != password_conf:
            raise serializers.ValidationError("Passwords mismatch")
        # Check if password is strong enough
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_active=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        token = self.gen_verification_token(user)
        subject = 'Verify your email at Personal CRM (PRM)'
        from_email = 'Personal CRM <noreply@prm.com>'
        content = render_to_string('emails/users/register_confirmation.html', {
            'user': user,
            'token': token,
            'type': 'email_confirmation',
        })
        message = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        message.send()

    def gen_verification_token(self, user):
        """Generate JWT necessary for the user to authenticate its account"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': exp_date,
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()


class UserVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        """Verify the user has provided a valid token"""
        try:
            payload = jwt.decode(
                data['token'], settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('token has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_active = True
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """Validate if this is a valid user."""
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('invalid user credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is not active yet')
        self.context['user'] = user
        return data

    def save(self):
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key
