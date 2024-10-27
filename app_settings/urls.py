from django.urls import path

from app_settings.views import GlobalSettingsAPIView, AppSettingsAPIView, RolesAPIView, RolesDetailAPIView, OrganizationsAPIView, OrganizationsDetailAPIView, PositionsAPIView, PositionsDetailAPIView

urlpatterns = [
    path("global-settings/", GlobalSettingsAPIView.as_view(),
         name="global-settings"),
    path("app-settings/", AppSettingsAPIView.as_view(),
         name="app-settings"),
    path("roles/", RolesAPIView.as_view(), name="roles"),
    path("roles/<int:pk>", RolesDetailAPIView.as_view(), name="roles-detail"),
    path("organizations/", OrganizationsAPIView.as_view(), name="organizations"),
    path("organizations/<int:pk>", OrganizationsDetailAPIView.as_view(),
         name="organizations-detail"),
    path("positions/", PositionsAPIView.as_view(), name="positions"),
    path("positions/<int:pk>", PositionsDetailAPIView.as_view(),
         name="positions-detail"),
]
