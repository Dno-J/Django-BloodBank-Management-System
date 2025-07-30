# Import Django's form system
from django import forms

# Import built-in user creation form and user model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Import the extended Profile model (linked via OneToOneField to User)
from accounts.models import Profile

# For raising custom validation errors
from django.core.exceptions import ValidationError

# Captcha field for bot protection
from captcha.fields import CaptchaField

# Blood group choices used in the signup form
BLOOD_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

# Custom signup form that extends Django's built-in UserCreationForm
class CustomSignupForm(UserCreationForm):
    # Username field with validation hints and Bootstrap styling
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="Required. 5+ characters. Alphanumeric only.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Additional fields for the Profile model
    full_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # HTML5 date picker
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    city = forms.CharField()
    state = forms.CharField()
    pincode = forms.CharField(max_length=10)
    blood_group = forms.ChoiceField(choices=BLOOD_CHOICES)
    share_health_info = forms.BooleanField(required=False)  # Optional checkbox
    existing_conditions = forms.CharField(required=False)   # Optional text field
    ongoing_medication = forms.CharField(required=False)    # Optional text field

    # Captcha field to prevent automated signups
    captcha = CaptchaField()

    # Meta class defines which model and fields are used for the base User object
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    # Custom validation for username field
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Enforce minimum length and alphanumeric constraint
        if len(username) < 5 or not username.isalnum():
            raise ValidationError("Username must be at least 5 characters long and alphanumeric.")
        # Check for uniqueness
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Override save method to create both User and Profile objects
    def save(self, commit=True):
        # Save User object without committing to DB yet
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Ensure email is saved

        if commit:
            user.save()  # Save User to DB
            # Create associated Profile with extended fields
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                phone_number=self.cleaned_data['phone_number'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                pincode=self.cleaned_data['pincode'],
                blood_group=self.cleaned_data['blood_group'],
                share_health_info=self.cleaned_data['share_health_info'],
                existing_conditions=self.cleaned_data['existing_conditions'],
                ongoing_medication=self.cleaned_data['ongoing_medication'],
            )
        return user
