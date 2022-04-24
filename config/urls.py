from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('src.accounts.djoser_token_urls')),

    path('', include('src.accounts.urls')),
    path('', include('src.projects.urls')),
    path('', include('src.main.urls')),
    path('', include('src.tests.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
