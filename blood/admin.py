# Django admin interface utilities
from django.contrib import admin

# Import models to be managed via admin panel
from .models import Donor, BloodRequest

# 🛠️ Register Donor model with admin site
admin.site.register(Donor)
# ✅ Enables viewing, adding, editing, and deleting donor records via admin

# 🛠️ Register BloodRequest model with admin site
admin.site.register(BloodRequest)
# ✅ Allows staff to manage blood requests directly from the admin dashboard
