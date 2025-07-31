from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('healthz/', health_check, name='healthz'),        # ✅ Must be before '' include
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),           # User login/dashboard
    path('blood/', include('blood.urls')),                 # Admin and donation flows
    path('captcha/', include('captcha.urls')),             # reCAPTCHA support
    path('', include('accounts.urls')),                    # Landing page: signup (placed last to avoid shadowing)
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
