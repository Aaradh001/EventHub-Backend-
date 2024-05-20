
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.api.client.urls')),
    path('token/', include('accounts.urls')),
    path('vendor/', include('accounts.api.vendor.urls')),
    path('event/', include('events.api.urls')),
    path('services/', include('services.api.urls')),
    path('admin-control/', include('admin_control.api.urls')),
    path('venue/', include('venue_management.api.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)