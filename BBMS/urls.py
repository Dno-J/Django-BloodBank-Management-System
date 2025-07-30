from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # login, signup, dashboard, etc.
    path('blood/', include('blood.urls')),        # donor and request forms
    path('captcha/', include('captcha.urls')),    # django-simple-captcha
]

# Only serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
