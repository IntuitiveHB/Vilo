from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from authentication.utils import Util
from rest_framework.fields import ChoiceField

from authentication.enums import UserTypes, ClientTypes
from app_settings.models import UserOrganization, UserPosition


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    # max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255)
    full_name = serializers.CharField(max_length=255, min_length=6)
    type = ChoiceField(choices=UserTypes._member_names_)
    phone_no = serializers.CharField(max_length=20, allow_null=True)
    address = serializers.CharField(max_length=100, allow_null=True)
    notes = serializers.CharField(allow_null=True)
    client_type = ChoiceField(
        choices=ClientTypes._member_names_, allow_blank=True)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=UserOrganization.objects.all(), allow_null=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=UserPosition.objects.all(), allow_null=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if get_user_model().objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError(
                {'email', ('Email already in use.')})
        return lower_email

    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'type', 'phone_no', 'address',
                  'notes', 'client_type', 'organization', 'position']

    def validate(self, attrs):
        type = attrs.get('type', '')
        client_type = attrs.get('client_type', '')
        organization = attrs.get('organization', '')
        position = attrs.get('position', '')

        if type == UserTypes.CLIENT.name:
            if not client_type or client_type == "":
                raise serializers.ValidationError(
                    {'client_type': ('Client type is required.')})
            if client_type == ClientTypes.COMPANY.name:
                if not organization or organization == "":
                    raise serializers.ValidationError(
                        {'organization': ('Client organization is required.')})

                if not position or position == "":
                    raise serializers.ValidationError(
                        {'position': ('Client position is required.')})

        return super().validate(attrs)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = get_user_model()
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email.lower(), password=password)

        if not user:
            raise AuthenticationFailed("Invaled Credentials, try again.")

        if not user.is_verified:
            raise AuthenticationFailed(
                "Email is not verified, contact administrator.")

        if not user.is_active:
            raise AuthenticationFailed(
                "Account disabled, contact administrator.")

        return {
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    default_error_message = {
        "bad_token": ('Token is expired or invalid.')
    }

    class Meta:
        model = get_user_model()
        fields = ['refresh']

    def validate(self, attrs):
        self.refresh = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh).blacklist()
        except TokenError as identifier:
            self.fail('bad_token')


class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is not registered.')})

        return super().validate(attrs)


class PasswordTokenCheckSerializer(serializers.ModelSerializer):
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid.', 401)

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid.', 401)

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid.', 401)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid.', 401)

        return super().validate(attrs)


class ChangePasswordSerailizer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    password2 = serializers.CharField(
        min_length=8, max_length=68, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        if not password:
            raise serializers.ValidationError(
                {'password': ('Password must be provided.')})

        if not password2:
            raise serializers.ValidationError(
                {'password': ('Confirm password must be provided.')})

        if not password == password2:
            raise serializers.ValidationError(
                {'password': ('Password and Confirm Password do not match.')})

        return super().validate(attrs)


class UserSerailizer(serializers.ModelSerializer):
    active = serializers.BooleanField(source="is_active")

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'full_name', 'type', 'phone_no', 'address',
                  'notes', 'client_type', 'organization', 'position', 'active']
        # fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'type', 'phone_no', 'address',
                  'notes', 'client_type', 'organization', 'position']

    def validate_email(self, value):
        user = self.context['request'].user
        if get_user_model().objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        '''
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})
        '''

        instance.full_name = validated_data.get(
            'full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.type = validated_data.get('type', instance.type)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.address = validated_data.get('address', instance.address)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.client_type = validated_data.get(
            'client_type', instance.client_type)
        instance.organization = validated_data.get(
            'organization', instance.organization)
        instance.position = validated_data.get('position', instance.position)
        instance.save()

        return instance


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email']
