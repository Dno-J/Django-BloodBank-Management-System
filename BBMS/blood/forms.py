# Django form utilities
from django import forms

# Built-in user creation form and user model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Import donor and blood request models
from .models import Donor, BloodRequest

# For raising custom validation errors
from django.core.exceptions import ValidationError


# -------------------------------
# 🔐 Custom Signup Form (if used in blood app)
# -------------------------------
class CustomUserCreationForm(UserCreationForm):
    # Username field with Bootstrap styling and validation hints
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Required. 5+ characters. Alphanumeric only."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Custom username validation
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            if len(username) < 5:
                raise ValidationError("Username must be at least 5 characters long.")
            if ' ' in username:
                raise ValidationError("Username cannot contain spaces.")
            if not username.isalnum():
                raise ValidationError("Username must be alphanumeric.")
            if User.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")

        return username


# -------------------------------
# 🩸 Blood Type Choices
# -------------------------------
BLOOD_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]


# -------------------------------
# 🩸 Donor Form
# -------------------------------
class DonorForm(forms.ModelForm):
    # Blood type dropdown with Bootstrap styling
    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Blood Type"
    )

    class Meta:
        model = Donor
        fields = ['blood_type', 'location', 'units_donated', 'available', 'notes']

        # Apply Bootstrap styling to all fields
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'units_donated': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# -------------------------------
# 🧾 Blood Request Form
# -------------------------------
class BloodRequestForm(forms.ModelForm):
    # Blood type dropdown with Bootstrap styling
    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Blood Type"
    )

    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'age', 'blood_type',
            'location', 'quantity_needed', 'contact'
        ]

        # Apply Bootstrap styling to all fields
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_needed': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # Custom validation for contact number
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact
