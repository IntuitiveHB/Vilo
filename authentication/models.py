from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from app_settings.models import UserPosition, UserOrganization
from authentication.enums import UserTypes, ClientTypes
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email.lower(), **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    # first_name = models.CharField(_('first name'))
    # last_name = models.CharField(_('last name'))
    full_name = models.CharField(_('full name'), null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_internal = models.BooleanField(default=True)
    is_client = models.BooleanField(default=False)

    type = models.CharField(_('Type'), max_length=50, choices=UserTypes.choices(),
                            # Default is internal user
                            default=UserTypes.INTERNAL.value)
    phone_no = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True)
    client_type = models.CharField(
        _('Client Type'), max_length=50, choices=ClientTypes.choices(), null=True)
    organization = models.ForeignKey(
        UserOrganization, related_name='organization', on_delete=models.DO_NOTHING, null=True)
    position = models.ForeignKey(
        UserPosition, related_name='position', on_delete=models.DO_NOTHING, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_internal

    def has_module_perms(self, app_label):
        return True

    '''def save(self, *args, **kwargs):
        if not self.type or self.type == None:
            self.type = CustomUser.Types.INTERNAL
        return super().save(*args, **kwargs)'''

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
