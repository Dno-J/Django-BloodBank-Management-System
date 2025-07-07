from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=100)  # Donor's name
    age = models.IntegerField()  # Donor's age
    blood_type = models.CharField(max_length=5)  # Blood group (e.g., A+, B-)
    location = models.CharField(max_length=100)  # Donor's location
    quantity_donated = models.PositiveIntegerField(help_text="Quantity donated in mL")  # Amount in mL
    contact = models.CharField(max_length=15, default='')  # Contact number
    donated_date = models.DateField(auto_now_add=True)  # Auto-set on creation

    def __str__(self):
        return f"{self.name} - {self.blood_type} ({self.quantity_donated} mL)"


class BloodRequest(models.Model):
    patient_name = models.CharField(max_length=100)  # Patient's name
    age = models.IntegerField()  # Patient's age
    blood_type = models.CharField(max_length=5)  # Requested blood group
    location = models.CharField(max_length=100)  # Location of patient
    quantity_needed = models.PositiveIntegerField(help_text="Quantity needed in mL")  # Amount in mL
    contact = models.CharField(max_length=15, default='')  # Contact number
    requested_date = models.DateField(auto_now_add=True)  # Auto-set on creation

    def __str__(self):
        return f"{self.patient_name} needs {self.blood_type} ({self.quantity_needed} mL)"
