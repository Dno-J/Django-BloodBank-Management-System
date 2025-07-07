from django.contrib import admin
from .models import Donor, BloodRequest

# Register models here
admin.site.register(Donor)
admin.site.register(BloodRequest)
