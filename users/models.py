from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .manager import CustomUserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ("A", _("Admin")),
        ("C", _("Customer")),
    )
    
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.get_full_name()}"
    
    class Meta:
        db_table = "users"
        ordering = ["-id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
