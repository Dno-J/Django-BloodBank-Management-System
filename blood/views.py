# Django utilities for rendering, redirecting, and object retrieval
from django.shortcuts import render, redirect, get_object_or_404

# Authentication helpers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# ORM aggregation and HTTP responses
from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.views.decorators.http import require_POST

# Data structures
from collections import defaultdict

# Axes model for tracking failed login attempts
from axes.models import AccessAttempt

# App models and forms
from .models import Donor, BloodRequest
from .forms import DonorForm, BloodRequestForm, CustomUserCreationForm
from accounts.models import Profile

# PDF generation
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile, os


# -------------------------------
# 📄 PDF Export View
# -------------------------------
@staff_member_required(login_url='admin_login')
def download_report_pdf(request):
    donors = Donor.objects.all()
    requests = BloodRequest.objects.all()

    # Summarize blood data
    donor_summary, request_summary, available_summary, blood_types = summarize_blood_data(donors, requests)

    context = {
        'donor_blood_summary': donor_summary,
        'request_blood_summary': request_summary,
        'available_blood_summary': available_summary,
        'blood_types': blood_types,
    }

    # Render HTML template to string
    html_string = render_to_string('report_template.html', context)

    # Create temporary file path
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf_path = tmp_file.name

    # Generate PDF from HTML
    HTML(string=html_string).write_pdf(target=pdf_path)

    # Serve PDF as HTTP response
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="blood_report.pdf"'

    os.remove(pdf_path)  # Clean up temp file
    return response


# -------------------------------
# 🧠 Blood Summary Helper
# -------------------------------
def summarize_blood_data(donors, requests):
    blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    donated_units = defaultdict(int)
    requested_ml = defaultdict(int)
    available_ml = defaultdict(int)

    # Aggregate donated units (as count)
    for donor in donors:
        bt = donor.blood_type.strip()
        if donor.available:
            donated_units[bt] += donor.units_donated or 0

    # Aggregate requested quantities (already in mL)
    for req in requests:
        bt = req.blood_type.strip()
        requested_ml[bt] += req.quantity_needed or 0

    # Calculate available blood in mL = donated_units * 450 - requested_ml
    for bt in blood_types:
        total_donated_ml = donated_units[bt] * 450
        total_requested_ml = requested_ml[bt]
        available_ml[bt] = max(0, total_donated_ml - total_requested_ml)

    return donated_units, requested_ml, available_ml, blood_types

# -------------------------------
# 🔐 Authentication Views
# -------------------------------
def signup_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'accounts/signup.html', {'form': form})

def landing_redirect(request):
    return redirect('signup')

def admin_login(request):
    warning = False
    failure_count = 0

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Count failed login attempts
        failure_count = AccessAttempt.objects.filter(username=username).count()
        if failure_count >= 3:
            warning = True

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('home')

        return render(request, 'admin_login.html', {
            'error': 'Invalid credentials or not staff',
            'warning': warning,
            'failure_count': failure_count,
        })

    return render(request, 'admin_login.html', {'warning': warning, 'failure_count': failure_count})

def custom_logout(request):
    logout(request)
    return redirect('admin_login')

def custom_lockout_response(request, credentials=None):
    return render(request, 'lockout.html', status=403)

@staff_member_required(login_url='admin_login')
def lockout_dashboard(request):
    if request.method == 'POST':
        AccessAttempt.objects.all().delete()
    attempts = AccessAttempt.objects.all().order_by('-attempt_time')
    return render(request, 'lockout_dashboard.html', {'attempts': attempts})


# -------------------------------
# 🌐 General Views
# -------------------------------
def about(request):
    return render(request, 'about.html')

@staff_member_required(login_url='admin_login')
def home(request):
    donors = Donor.objects.all()
    requests = BloodRequest.objects.all()

    donor_summary, request_summary, available_summary, blood_types = summarize_blood_data(donors, requests)

    context = {
        'recent_donors': donors.order_by('-id')[:5],
        'recent_requests': requests.order_by('-id')[:5],
        'total_donors': donors.count(),
        'total_requests': requests.count(),
        'verified_donors': donors.filter(verified=True),
        'unverified_donors': donors.filter(verified=False),
        'verified_requests': requests.filter(verified=True),
        'unverified_requests': requests.filter(verified=False),
        'donor_blood_summary': donor_summary,
        'request_blood_summary': request_summary,
        'available_blood_summary': available_summary,
        'blood_types': blood_types,
    }
    return render(request, 'home.html', context)


# -------------------------------
# 🏠 User Dashboard
# -------------------------------
@login_required(login_url='login')
def user_dashboard(request):
    donations = Donor.objects.filter(user=request.user).order_by('-donation_date')
    requests = BloodRequest.objects.filter(user=request.user).order_by('-requested_date')
    return render(request, 'accounts/dashboard.html', {
        'donations': donations,
        'requests': requests,
    })


# -------------------------------
# 🩸 Donor Views
# -------------------------------
@login_required(login_url='login')
def register_donor(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.blood_type = profile.blood_group  # Auto-fill from profile
            donor.save()
            return redirect('user_dashboard')
    else:
        form = DonorForm()

    return render(request, 'register_donor.html', {
        'form': form,
        'profile': profile
    })

@require_POST
@staff_member_required(login_url='admin_login')
def delete_donor(request, id):
    donor = get_object_or_404(Donor, pk=id)
    donor.delete()
    return redirect('home')

@require_POST
@staff_member_required(login_url='admin_login')
def toggle_verification(request, id):
    donor = get_object_or_404(Donor, pk=id)
    donor.verified = not donor.verified
    donor.save()
    return redirect('home')


# -------------------------------
# 🚨 Blood Request Views
# -------------------------------
@login_required(login_url='login')
def request_blood(request):
    form = BloodRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        req = form.save(commit=False)
        req.user = request.user
        req.save()
        return redirect('home')
    return render(request, 'request_blood.html', {'form': form})

@require_POST
@staff_member_required(login_url='admin_login')
def delete_requester(request, id):
    requester = get_object_or_404(BloodRequest, pk=id)
    requester.delete()
    return redirect('home')

@require_POST
@staff_member_required(login_url='admin_login')
def toggle_request_verification(request, id):
    req = get_object_or_404(BloodRequest, pk=id)
    req.verified = not req.verified
    req.save()
    return redirect('home')
