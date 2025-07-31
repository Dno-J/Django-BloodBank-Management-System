from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    landing_redirect,    # 👈 NEW view for landing page redirect
    signup_view,
    custom_login_view,
    user_dashboard,
    profile_view,
    register_donor,
    request_blood,
    admin_login_view,    # ✅ NEW: Import admin login view
)

urlpatterns = [
    # 🔄 Redirect root / to /signup/
    path('', landing_redirect, name='landing_redirect'),

    # 📝 User registration
    path('signup/', signup_view, name='signup'),

    # 🔐 Login + Logout
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 🧾 Dashboard + Profile
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('profile/', profile_view, name='profile'),

    # 🩸 Donor + Request Forms
    path('donate/', register_donor, name='register_donor'),
    path('request/', request_blood, name='request_blood'),

    # ✅ Custom Admin Login Page (not Django admin)
    path('admin-login/', admin_login_view, name='admin_login'),
]
