from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'A')
        extra_fields.setdefault('phone', '-')
        extra_fields.setdefault('address', '-')
        return super().create_superuser(username, email, password, **extra_fields)
