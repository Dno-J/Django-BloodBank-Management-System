from django.shortcuts import render, redirect, get_object_or_404  # Rendering and redirecting views
from django.contrib.auth import authenticate, login, logout       # Auth functions
from django.contrib.auth.decorators import login_required         # To protect views
from django.db.models import Sum                                  # For blood quantity aggregation
from .models import Donor, BloodRequest                           # Import models
from .forms import DonorForm, BloodRequestForm                    # Import forms

# ---------------- AUTH ----------------
def custom_logout(request):  # Logs out the admin
    logout(request)
    return redirect('admin_login')

def admin_login(request):  # Admin login logic
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('home')  # After login, redirect to homepage
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not staff'})
    return render(request, 'admin_login.html')


# ---------------- GENERAL PAGES ----------------
def about(request):  # Static About page
    return render(request, 'about.html')

@login_required(login_url='admin_login')
def home(request):  # Homepage showing blood availability
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    availability = {}
    for group in blood_groups:
        donated = Donor.objects.filter(blood_type=group).aggregate(total=Sum('quantity_donated'))['total'] or 0
        requested = BloodRequest.objects.filter(blood_type=group).aggregate(total=Sum('quantity_needed'))['total'] or 0
        availability[group] = max(donated - requested, 0)
    return render(request, 'home.html', {'availability': availability})


# ---------------- DONOR ----------------
@login_required(login_url='admin_login')
def register_donor(request):  # Register a new blood donor
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DonorForm()
    return render(request, 'register_donor.html', {'form': form})

@login_required(login_url='admin_login')
def donators_info(request):  # View all donors
    donors = Donor.objects.all()
    return render(request, 'donators_info.html', {'donors': donors})

@login_required(login_url='admin_login')
def delete_donor(request, id):  # Delete donor by ID
    donor = get_object_or_404(Donor, pk=id)
    donor.delete()
    return redirect('donators_info')


# ---------------- BLOOD REQUEST ----------------
@login_required(login_url='admin_login')
def request_blood(request):  # Submit blood request
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BloodRequestForm()
    return render(request, 'request_blood.html', {'form': form})

@login_required(login_url='admin_login')
def requesters_info(request):  # View all blood requests
    requests = BloodRequest.objects.all()
    return render(request, 'requesters_info.html', {'requests': requests})

@login_required(login_url='admin_login')
def delete_requester(request, id):  # Delete request by ID
    requester = get_object_or_404(BloodRequest, pk=id)
    requester.delete()
    return redirect('requesters_info')
