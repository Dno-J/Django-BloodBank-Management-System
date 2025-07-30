from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="homepage.html"), name='home'),
    path('healthz/', lambda request: HttpResponse("OK"), name='healthz'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blood/', include('blood.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
