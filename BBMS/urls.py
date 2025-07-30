from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="homepage.html"), name='home'),  # 🚀 Homepage route
    path('healthz/', lambda request: HttpResponse("OK"), name='healthz'),        # ❤️ Health check for Render

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blood/', include('blood.urls')),
    path('captcha/', include('captcha.urls')),
]


# Only serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
