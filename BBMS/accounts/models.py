# Import Django's model system
from django.db import models

# Import built-in User model for authentication
from django.contrib.auth.models import User

# Profile model extends the built-in User model with additional health and contact info
class Profile(models.Model):
    # One-to-one relationship with User; deletes Profile if User is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Full name of the user (used for display and identification)
    full_name = models.CharField(max_length=100)

    # Optional date of birth field
    date_of_birth = models.DateField(null=True, blank=True)

    # Gender selection with predefined choices
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    )

    # Contact and location details
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Blood group stored as a short string (e.g., "A+", "O-")
    blood_group = models.CharField(max_length=3)

    # Checkbox to indicate if user consents to share health info
    share_health_info = models.BooleanField(default=False)

    # Optional health-related fields
    existing_conditions = models.TextField(blank=True)     # e.g., diabetes, hypertension
    ongoing_medication = models.TextField(blank=True)      # e.g., insulin, blood thinners

    # String representation used in admin and debugging
    def __str__(self):
        return self.full_name
