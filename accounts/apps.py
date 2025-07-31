from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        try:
            User = get_user_model()
            demo_username = "admin"
            demo_password = "admin123"
            demo_email = "admin@demo.com"

            if not User.objects.filter(username=demo_username).exists():
                User.objects.create_superuser(demo_username, demo_email, demo_password)
                print("✅ Created default admin user: admin / admin123")
            else:
                print("ℹ️ Admin user already exists.")
        except (OperationalError, ProgrammingError):
            # Happens during migration or first deploy when DB isn't ready
            pass
