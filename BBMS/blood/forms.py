from django import forms
from .models import Donor, BloodRequest

# Choices available in dropdown for blood types
BLOOD_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

# -------------------------------
# Donor Form
# -------------------------------
class DonorForm(forms.ModelForm):
    # Blood type is rendered as a dropdown select box
    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})  # Bootstrap class for styling
    )

    class Meta:
        model = Donor  # Form is built from Donor model
        fields = ['name', 'age', 'blood_type', 'location', 'quantity_donated', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Standard input with Bootstrap
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_donated': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity in mL'  # User hint
            }),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# Blood Request Form
# -------------------------------
class BloodRequestForm(forms.ModelForm):
    # Same dropdown for blood type
    blood_type = forms.ChoiceField(
        choices=BLOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = BloodRequest  # Based on BloodRequest model
        fields = ['patient_name', 'age', 'blood_type', 'location', 'quantity_needed', 'contact']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_needed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity in mL'
            }),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }