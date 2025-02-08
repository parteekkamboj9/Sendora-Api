from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: JsonResponse({"status": "Running"})),
    path('api/', include('sendoraApp.urls')),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
