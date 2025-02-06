from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

urlpatterns = [
    path('', lambda request: JsonResponse({"status": "Running"})),
    path('api/', include('sendoraApp.urls')),
    path('admin/', admin.site.urls),
]
