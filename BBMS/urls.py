from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from blood.views import home  # ✅ Import the admin dashboard view

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('healthz/', health_check, name='healthz'),         # ✅ Health check endpoint
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),            # User login/dashboard
    path('blood/', include('blood.urls')),                  # Donor/request flows
    path('captcha/', include('captcha.urls')),              # reCAPTCHA support
    path('admin-dashboard/', home, name='admin_dashboard'), # ✅ Admin dashboard view
    path('', include('accounts.urls')),                     # Default: signup
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
