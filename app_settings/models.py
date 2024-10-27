from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class GlobalSettings(models.Model):
    application_name = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=32, default='UTC')
    date_format = models.CharField(max_length=20, default='%Y-%m-%d')
    services = ArrayField(models.CharField())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.application_name


class AppSettings(models.Model):
    tax_label = models.CharField(max_length=255)
    # Client Reference Number (CRN)
    crn_format = models.CharField(max_length=50)
    # File Reference Number (FRN)
    frn_format = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tax_label


class UserRole(models.Model):
    role_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


class UserOrganization(models.Model):
    organization_name = models.CharField(max_length=100)
    organization_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name


class UserPosition(models.Model):
    position_name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        UserOrganization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_name
