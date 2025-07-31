from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('healthz/', health_check, name='healthz'),  # ✅ Health check

    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('blood/', include('blood.urls')),
    path('captcha/', include('captcha.urls')),
]

# (Optional) Add static/media in dev mode
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
