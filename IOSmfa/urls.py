from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
# Django mfa
import mfa
import mfa.TrustedDevice


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mfa/', include('mfa.urls')), #required to use mfa
    path('devices/add/', mfa.TrustedDevice.add, name="mfa_add_new_trusted_device"), #required if you intend adding some devices
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "IOSmfa MANAGEMENT"
admin.site.site_title = "IOSmfa STUFF"
admin.site.index_title = "IOSmfa Admin Panel"
