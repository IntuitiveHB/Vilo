from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from authentication.views import (
    RegisterAPIView, VerifyEmail, LoginAPIView, LogoutAPIView, RequestPasswordResetEmailAPIView,
    PasswordTokenCheckAPIView, SetNewPasswordAPIView, ChangePasswordAPIView, ResendVerifyEmail,
    UsersListView, ClientsListView, UpdateProfileView
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("email-verify", VerifyEmail.as_view(), name="email-verify"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("request-reset-email/", RequestPasswordResetEmailAPIView.as_view(),
         name="request-reset-email"),
    path("password-reset/",
         PasswordTokenCheckAPIView.as_view(), name="password-reset-confirm"),
    path("password-reset-complete/", SetNewPasswordAPIView.as_view(),
         name="password-reset-complete"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("resend-verification/", ResendVerifyEmail.as_view(),
         name="resend-verification"),
    path("users/", UsersListView.as_view(), name="users-list"),
    path("clients/", ClientsListView.as_view(), name="clients-list"),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
]
