# Import path function to define URL patterns
from django.urls import path

# Import built-in authentication views (used for logout here)
from django.contrib.auth import views as auth_views

# Import custom views from the current app
from .views import (
    signup_view,         # Handles user registration
    custom_login_view,   # Custom login logic and UI
    user_dashboard,      # Main dashboard after login
    profile_view,        # Displays user profile info
    register_donor,      # Form to register as a blood donor
    request_blood,       # Form to request blood
)

# Define URL patterns for the accounts app
urlpatterns = [
    # User registration page
    path('signup/', signup_view, name='signup'),

    # Custom login page
    path('login/', custom_login_view, name='login'),

    # Logout view using Django's built-in LogoutView
    # Redirects to login page after logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard shown after successful login
    path('dashboard/', user_dashboard, name='user_dashboard'),

    # Profile view for user details
    path('profile/', profile_view, name='profile'),

    # Donor registration form
    path('donate/', register_donor, name='register_donor'),

    # Blood request form
    path('request/', request_blood, name='request_blood'),
]
