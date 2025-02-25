from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    username = None  # Remove username field
    last_login = None  # Remove last_login field
    is_staff = None  # Remove is_staff field
    is_superuser = None  # Remove is_superuser field

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128)  # Hashed password

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customer_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customer_users_permissions", 
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
