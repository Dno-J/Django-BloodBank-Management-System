from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),                            # Admin login page
    path('admin-logout/', views.custom_logout, name='admin_logout'),                        # Admin logout action

    path('', views.home, name='home'),                                                      # Homepage (blood availability)
    path('about/', views.about, name='about'),                                              # About Me page
    path('register/', views.register_donor, name='register_donor'),                         # Donor registration form
    path('request/', views.request_blood, name='request_blood'),                            # Blood request form
    path('donors-info/', views.donators_info, name='donators_info'),                        # View all donor records
    path('requesters-info/', views.requesters_info, name='requesters_info'),                # View all requester records
    path('delete-donor/<int:id>/', views.delete_donor, name='delete_donor'),                # Delete a donor by ID
    path('delete-requester/<int:id>/', views.delete_requester, name='delete_requester'),    # Delete a requester by ID
]
