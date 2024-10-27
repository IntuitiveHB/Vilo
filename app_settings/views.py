from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from app_settings.serializers import GlobalSettingSerializer, AppSettingSerializer, UserRoleSerializer, UserOrganizationSerializer, UserPositionSerializer
from app_settings.models import GlobalSettings, AppSettings, UserRole, UserOrganization, UserPosition
# Create your views here.


class GlobalSettingsAPIView(GenericAPIView):
    serializer_class = GlobalSettingSerializer

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        setting = request.data
        serializer = self.serializer_class(data=setting)

        if serializer.is_valid(raise_exception=True):
            setting_data = GlobalSettings.objects.first()
            if setting_data:
                serializer.update(
                    setting_data, serializer.validated_data)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        settings_data = GlobalSettings.objects.first()

        if settings_data:
            serializer = self.serializer_class(settings_data)
            return Response(serializer.data, status=status.HTTP_200_OK)


class AppSettingsAPIView(GenericAPIView):
    serializer_class = AppSettingSerializer

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        setting = request.data
        serializer = self.serializer_class(data=setting)

        if serializer.is_valid(raise_exception=True):
            setting_data = AppSettings.objects.first()
            if setting_data:
                serializer.update(
                    setting_data, serializer.validated_data)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        settings_data = AppSettings.objects.first()

        if settings_data:
            serializer = self.serializer_class(settings_data)
            return Response(serializer.data, status=status.HTTP_200_OK)


class RolesAPIView(GenericAPIView):
    serializer_class = UserRoleSerializer

    # permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        role = request.data
        serializer = self.serializer_class(data=role)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        roles = UserRole.objects.all()

        if roles:
            serializer = self.serializer_class(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class RolesDetailAPIView(GenericAPIView):
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )

    def get_role(self, pk):
        try:
            return UserRole.objects.get(pk=pk)
        except:
            None

    def get(self, request, pk):
        role = self.get_role(pk=pk)

        if role == None:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        role = self.get_role(pk=pk)

        if role == None:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_role(pk=pk)
        if role == None:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        role.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationsAPIView(GenericAPIView):
    serializer_class = UserOrganizationSerializer

    # permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        organization = request.data
        serializer = self.serializer_class(data=organization)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        organizations = UserOrganization.objects.all()

        if organizations:
            serializer = self.serializer_class(organizations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class OrganizationsDetailAPIView(GenericAPIView):
    serializer_class = UserOrganizationSerializer
    queryset = UserOrganization.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )

    def get_organization(self, pk):
        try:
            return UserOrganization.objects.get(pk=pk)
        except:
            None

    def get(self, request, pk):
        organization = self.get_organization(pk=pk)

        if organization == None:
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        organization = self.get_organization(pk=pk)

        if organization == None:
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            organization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        organization = self.get_organization(pk=pk)
        if organization == None:
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        organization.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PositionsAPIView(GenericAPIView):
    serializer_class = UserPositionSerializer

    # permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        position = request.data
        serializer = self.serializer_class(data=position)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        positions = UserPosition.objects.all()

        if positions:
            serializer = self.serializer_class(positions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class PositionsDetailAPIView(GenericAPIView):
    serializer_class = UserPositionSerializer
    queryset = UserPosition.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )

    def get_position(self, pk):
        try:
            return UserPosition.objects.get(pk=pk)
        except:
            None

    def get(self, request, pk):
        position = self.get_position(pk=pk)

        if position == None:
            return Response({"message": "Position not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(position)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        position = self.get_position(pk=pk)

        if position == None:
            return Response({"message": "Position not found"}, status=status.HTTP_404_NOT_FOUND)

        if not UserOrganization.objects.filter(pk=request.data["organization"]).exists():
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            position, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        position = self.get_position(pk=pk)
        if position == None:
            return Response({"message": "Position not found"}, status=status.HTTP_404_NOT_FOUND)
        position.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
