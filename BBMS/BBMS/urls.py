from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django admin panel (default)
    path('', include('blood.urls')),         # Includes all app-level routes from blood/urls.py
]