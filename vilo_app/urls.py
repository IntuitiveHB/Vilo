from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="VILO API",
        default_version='v1',
        description="API documentation for development, testing and validation.",
        terms_of_service="https://www.vilo.nestvested.co/policies/terms/",
        contact=openapi.Contact(email="no-reply@nestvested.co.uk"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('authentication.urls')),
    path('api_docs/swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('api_docs/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path("settings/", include('app_settings.urls')),
    path("task_management/", include('task_management.urls')),
    path('conversations/', include('chat.urls')),
]
