# Django's admin and URL routing utilities
from django.contrib import admin
from django.urls import path, include

# Import homepage view from blood app
from blood import views

# 🔗 Root URL configuration for the BBMS project
urlpatterns = [
    # 🌐 Homepage route
    path('', views.home, name='home'),
    # 👈 Admin dashboard

    # 🛠️ Django admin interface
    path('admin/', admin.site.urls),

    # 🩸 Blood-related routes (donation, request, summary)
    path('blood/', include('blood.urls')),
    # ✅ Keeps blood app modular and organized under /blood/

    # 👤 User account routes (signup, login, dashboard)
    path('accounts/', include('accounts.urls')),

    # 🤖 Captcha routes (used in signup form)
    path('captcha/', include('captcha.urls')),
]
