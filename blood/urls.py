# Django URL routing utilities
from django.urls import path

# Import views from current app
from . import views

# Optional: built-in logout view (not used here since custom logout is defined)
from django.contrib.auth.views import LogoutView


# 🔗 URL patterns for blood app
urlpatterns = [
    # -------------------------------
    # 🔐 Admin Access
    # -------------------------------
    path('admin-login/', views.admin_login, name='admin_login'),
    # ✅ Custom admin login view (separate from user login)

    path('admin-logout/', views.custom_logout, name='admin_logout'),
    # ✅ Custom logout view for admin users


    # -------------------------------
    # 🔐 Security & Lockouts
    # -------------------------------
    path('lockouts/', views.lockout_dashboard, name='lockout_dashboard'),
    # ✅ Displays locked-out users (via Axes), for admin review


    # -------------------------------
    # 🌐 Public Pages
    # -------------------------------
    path('', views.home, name='home'),
    # ✅ Homepage (landing page)

    path('about/', views.about, name='about'),
    # ✅ About page (project info, contact, etc.)

    path('signup/', views.signup_view, name='signup'),
    # ✅ Public signup route (can be reused or redirected)


    # -------------------------------
    # 🩸 Donor Flow
    # -------------------------------
    path('register/', views.register_donor, name='register_donor'),
    # ✅ Donor registration form

    path('delete-donor/<int:id>/', views.delete_donor, name='delete_donor'),
    # ✅ Admin-only route to delete donor record by ID


    # -------------------------------
    # 🚨 Requester Flow
    # -------------------------------
    path('request/', views.request_blood, name='request_blood'),
    # ✅ Blood request form

    path('delete-requester/<int:id>/', views.delete_requester, name='delete_requester'),
    # ✅ Admin-only route to delete blood request by ID


    # -------------------------------
    # ✅ Verification Toggles
    # -------------------------------
    path('toggle-verification/<int:id>/', views.toggle_verification, name='toggle_verification'),
    # ✅ Admin toggle for donor verification status

    path('toggle-request-verification/<int:id>/', views.toggle_request_verification, name='toggle_request_verification'),
    # ✅ Admin toggle for blood request verification status


    # -------------------------------
    # 📄 PDF Report
    # -------------------------------
    path('report/pdf/', views.download_report_pdf, name='download_report_pdf'),
    # ✅ Generates and downloads PDF summary of donations/requests
]
