from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import API_VERSION

schema_view = get_schema_view(
    openapi.Info(
        title="TeamUp API",
        default_version=API_VERSION,
        description="Full api to contribute with TeamUp services",
        contact=openapi.Contact(email="dashagarov@edu.hse.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
