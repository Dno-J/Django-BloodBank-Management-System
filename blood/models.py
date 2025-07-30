# Django model utilities
from django.db import models

# Built-in User model for authentication
from django.contrib.auth.models import User


# -------------------------------
# 🩸 Donor Model
# -------------------------------
class Donor(models.Model):
    # Blood type choices for donor registration
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    # Link to the logged-in user who is donating
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Donor's blood group (selected from predefined choices)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES)

    # Auto-set donation date when record is created
    donation_date = models.DateField(auto_now_add=True)

    # Location where donation is made (e.g., hospital, city)
    location = models.CharField(max_length=100)

    # Number of units donated (1 unit ≈ 450 mL)
    units_donated = models.PositiveIntegerField(
        default=1,
        help_text="Units donated (1 unit ≈ 450 mL)"
    )

    # Indicates if donor is currently available and healthy
    available = models.BooleanField(default=True)

    # Optional notes (e.g., availability time, health remarks)
    notes = models.TextField(blank=True)

    # Staff verification flag (used in admin dashboard)
    verified = models.BooleanField(default=False)

    # String representation used in admin and logs
    def __str__(self):
        return f"{self.user.username} - {self.donation_date} ({self.units_donated} units)"


# -------------------------------
# 🧾 Blood Request Model
# -------------------------------
class BloodRequest(models.Model):
    # Blood type choices for request form
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    # Link to the logged-in user making the request
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Patient details
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()

    # Requested blood group
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES)

    # Location where blood is needed
    location = models.CharField(max_length=100)

    # Quantity needed in milliliters
    quantity_needed = models.PositiveIntegerField(help_text="Quantity needed in mL")

    # Contact number for coordination
    contact = models.CharField(max_length=15, default='')

    # Auto-set request date when record is created
    requested_date = models.DateField(auto_now_add=True)

    # Staff verification flag (used in admin dashboard)
    verified = models.BooleanField(default=False)

    # String representation used in admin and logs
    def __str__(self):
        return f"{self.patient_name} needs {self.blood_type} ({self.quantity_needed} mL)"
