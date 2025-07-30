# Django's admin and URL routing utilities
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Import homepage view from blood app
from blood import views

# 🩺 Health check view
def health_check(request):
    return HttpResponse("OK")

# 🔗 Root URL configuration for the BBMS project
urlpatterns = [
    # 🌐 Homepage route
    path('', views.home, name='home'),

    # 🛠️ Django admin interface
    path('admin/', admin.site.urls),

    # 🩸 Blood-related routes (donation, request, summary)
    path('blood/', include('blood.urls')),

    # 👤 User account routes (signup, login, dashboard)
    path('accounts/', include('accounts.urls')),

    # 🤖 Captcha routes (used in signup form)
    path('captcha/', include('captcha.urls')),

    # 🩺 Health check endpoint for Render
    path('healthz/', health_check),
]
