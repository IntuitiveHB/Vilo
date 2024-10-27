from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authentication.serializers import (
    RegisterSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer,
    RequestPasswordResetEmailSerializer, PasswordTokenCheckSerializer, SetNewPasswordSerializer,
    ChangePasswordSerailizer, UserSerailizer, UpdateUserSerializer
)

from authentication.utils import Util
# Create your views here.
from authentication.enums import UserTypes

from rest_framework.permissions import IsAuthenticated


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = serializer.data['email']
            type = serializer.data['type']
            user = get_user_model().objects.get(email=email)

            user.is_internal = True
            user.is_client = False
            if type == UserTypes.CLIENT.name:
                user.is_internal = False
                user.is_client = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', openapi.IN_QUERY, descritption='Description of Token', type=openapi.TYPE_STRING)
    user_response = openapi.Response('response description', serializer_class)

    @swagger_auto_schema(manual_parameters=[token_param_config], responses={200: user_response})
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()

            return Response({'email': 'Email successfully verified.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmailAPIView(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            user = get_user_model().objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request).domain
            '''relative_link = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})'''
            relative_link = '/set-new-password'
            protocol = 'https' if request.is_secure() else 'http'
            # absurl = protocol+'://'+...
            absurl = current_site + relative_link + '/' + uidb64 + '/' + token

            data = {
                'user': user.first_name,
                'email': user.email,
                'domain': absurl,
                'subject': 'Reset your password.',
                'template': 'email_reset_password_template.html',
            }

            Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(GenericAPIView):
    serializer_class = PasswordTokenCheckSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            try:
                id = smart_str(urlsafe_base64_decode(uidb64))
                user = get_user_model().objects.get(id=id)

                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response({'error': 'Token is not valid, please request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

                return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
            except DjangoUnicodeDecodeError as identifier:
                return Response({'error': 'Token is not valid, please request a new one.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerailizer

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            # user = get_user_model().objects.get(email=request.user.email)
            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({'success': True, 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyEmail(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            try:
                user_data = serializer.data
                user = get_user_model().objects.get(email=user_data['email'])
                if user.is_verified:
                    return Response({'msg': 'User is already verified'})

                token = RefreshToken.for_user(user).access_token

                current_site = get_current_site(request).domain
                # relative_link = reverse('email-verify')
                relative_link = '/email-verification'
                # protocol = 'https' if request.is_secure() else 'http'
                # absurl = protocol+'://'+ ...
                absurl = current_site + relative_link+"?token="+str(token)

                new_pass = Util.generate_random_password(16)
                user.set_password(new_pass)
                user.save(update_fields=['password'])

                data = {
                    'user': user.first_name,
                    'email': user.email,
                    'pwd': new_pass,
                    'domain': absurl,
                    'subject': 'Verify your email.',
                    'template': 'email_welcome_template.html',
                }

                Util.send_email(data)
                return Response({'msg': 'The verification email has been sent'}, status=status.HTTP_201_CREATED)
            except get_user_model().DoesNotExist:
                return Response({'msg': 'No such user, register first'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListView(ListAPIView):
    serializer_class = UserSerailizer
    queryset = get_user_model().objects.filter(is_superuser=False)
    # def get(self, request):


class ClientsListView(ListAPIView):
    serializer_class = UserSerailizer
    queryset = get_user_model().objects.filter(is_client=True)


class UpdateProfileView(UpdateAPIView):

    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
