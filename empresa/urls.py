#from django import urls
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework.authentication import BaseAuthentication
from rest_framework.routers import DefaultRouter

from company.views import CompanyViewSet
from register.views import ClientViewSet, UserViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version="v1",
        description="Desafio Hora da Pratica 02",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@xyz.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="User")
router.register(r"client", ClientViewSet, basename="Client")
router.register(r"company", CompanyViewSet, basename="Company")


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api-auth/", include("rest_framework.urls", namespace="v1")),
    re_path(r"^api/v1/", include(router.urls)),
    re_path(
        r"^swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


STATIC_ROOT = "/var/www/example.com/static/"
