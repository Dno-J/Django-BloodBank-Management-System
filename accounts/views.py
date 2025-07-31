from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse

from accounts.forms import CustomSignupForm
from accounts.models import Profile
from blood.models import Donor, BloodRequest
from blood.forms import DonorForm, BloodRequestForm


def landing_redirect(request):
    return redirect('signup')


def health_check(request):
    return HttpResponse("OK", status=200)


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                messages.success(request, "Signup successful! You can now log in.")
                login(request, user)
                return redirect('user_dashboard')
            except Exception as e:
                print(f"[ERROR] Signup failed: {e}")
                form.add_error(None, f"Unexpected error during signup: {e}")
        else:
            print("[INVALID FORM DATA]", form.errors)
    else:
        form = CustomSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            print("[LOGIN FAILED]", form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def user_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile data not found. Please contact support.")
        return redirect('logout')

    donations = Donor.objects.filter(user=request.user).order_by('-donation_date')
    requests = BloodRequest.objects.filter(user=request.user).order_by('-requested_date')

    return render(request, 'accounts/dashboard.html', {
        'donations': donations,
        'requests': requests,
        'profile': profile,
        'greeting': f"Welcome back, {profile.full_name or request.user.username}!",
    })


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def register_donor(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.blood_type = profile.blood_group
            donor.save()
            messages.success(request, "Thank you for registering as a donor!")
            return redirect('user_dashboard')
    else:
        form = DonorForm()

    return render(request, 'register_donor.html', {'form': form, 'profile': profile})


@login_required(login_url='login')
def request_blood(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.blood_type = profile.blood_group
            blood_request.save()
            messages.success(request, "Your blood request has been submitted.")
            return redirect('user_dashboard')
        else:
            print("[FORM ERRORS]", form.errors)
    else:
        form = BloodRequestForm()

    return render(request, 'request_blood.html', {'form': form, 'profile': profile})


# 🔐 Admin Login View (FIXED: shows form fields)
def admin_login_view(request):
    error = None
    warning = None
    failure_count = request.session.get('failure_count', 0)
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_staff:
                login(request, user)
                request.session['failure_count'] = 0  # Reset on success
                return redirect('admin_dashboard')
            else:
                failure_count += 1
                request.session['failure_count'] = failure_count
                if failure_count >= 5:
                    error = "You have been locked out due to too many failed attempts."
                else:
                    error = "Invalid credentials. Please try again."
                    warning = True

    return render(request, 'accounts/admin_login.html', {
        'form': form,
        'error': error,
        'warning': warning,
        'failure_count': failure_count,
    })
