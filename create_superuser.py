import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "pg_managementPRD.settings"
)

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superuser created")
    else:
        print("ℹ️ Superuser already exists")
else:
    print("⚠️ Superuser env vars not set")
