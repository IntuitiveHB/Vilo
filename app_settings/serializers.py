from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

from app_settings.models import GlobalSettings, AppSettings, UserRole, UserOrganization, UserPosition


class GlobalSettingSerializer(serializers.ModelSerializer):
    application_name = serializers.CharField(max_length=255)
    time_zone = serializers.CharField(max_length=32)
    date_format = serializers.CharField(max_length=20)
    services = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

    class Meta:
        model = GlobalSettings
        fields = ['application_name',
                  'time_zone', 'date_format', 'services']

    def validate(self, attrs):
        pass

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Create and return a new `Setting` instance, given the validated data.
        """
        return GlobalSettings.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.application_name = validated_data.get(
            'application_name', instance.application_name)
        instance.time_zone = validated_data.get(
            'time_zone', instance.time_zone)
        instance.date_format = validated_data.get(
            'date_format', instance.date_format)
        instance.services = validated_data.get('services', instance.services)
        instance.save()

        return instance


class AppSettingSerializer(serializers.ModelSerializer):
    tax_label = serializers.CharField(max_length=255)
    crn_format = serializers.CharField(max_length=50)
    frn_format = serializers.CharField(max_length=50)

    class Meta:
        model = AppSettings
        fields = ['tax_label', 'crn_format', 'frn_format']

    def validate(self, attrs):
        pass

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Create and return a new `Setting` instance, given the validated data.
        """
        return AppSettings.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tax_label = validated_data.get(
            'tax_label', instance.tax_label)
        instance.crn_format = validated_data.get(
            'crn_format', instance.crn_format)
        instance.frn_format = validated_data.get(
            'frn_format', instance.frn_format)
        instance.save()

        return instance


class UserRoleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(max_length=100)

    class Meta:
        model = UserRole
        fields = ['id', 'role_name']

    def validate(self, attrs):
        role_name = attrs.get('role_name', '')
        if UserRole.objects.filter(role_name=role_name).exists():
            raise serializers.ValidationError(
                {'role', ('Role already exists.')})

        return super().validate(attrs)

    def create(self, validated_data):
        return UserRole.objects.create(**validated_data)


class UserOrganizationSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(max_length=100)
    organization_address = serializers.CharField(max_length=255)

    class Meta:
        model = UserOrganization
        fields = ['id', 'organization_name', 'organization_address']

    def validate(self, attrs):
        organization_name = attrs.get('organization_name', '')
        if UserOrganization.objects.filter(organization_name=organization_name).exists():
            raise serializers.ValidationError(
                {'organization', ('Organization already exists.')})

        return super().validate(attrs)

    def create(self, validated_data):
        return UserOrganization.objects.create(**validated_data)


class UserPositionSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(max_length=255)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=UserOrganization.objects.all())

    class Meta:
        model = UserPosition
        fields = ['id', 'position_name', 'organization']

    def validate(self, attrs):
        position_name = attrs.get('position_name', '')
        organization = attrs.get('organization')

        if UserPosition.objects.filter(position_name=position_name).exists():
            raise serializers.ValidationError(
                {'poistion', ('Poistion already exists.')})

        if not UserOrganization.objects.filter(pk=organization.id).exists():
            raise serializers.ValidationError(
                {'organization', ('Organization does not exists.')})

        return super().validate(attrs)

    def create(self, validated_data):
        return UserPosition.objects.create(**validated_data)
