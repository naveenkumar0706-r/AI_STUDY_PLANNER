from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom user model. We extend AbstractUser instead of AbstractBaseUser
    so we keep Django's battle-tested auth (permissions, password hashing,
    admin integration) and simply add the extra profile fields the study
    planner needs (college, department, year, mobile number).
    """

    YEAR_CHOICES = [
        ("1", "1st Year"),
        ("2", "2nd Year"),
        ("3", "3rd Year"),
        ("4", "4th Year"),
        ("PG", "Postgraduate"),
    ]

    mobile_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Mobile number must be entered in the format: '+919999999999'. Up to 15 digits allowed.",
    )

    email = models.EmailField(unique=True)
    college = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, blank=True)
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    dark_mode_enabled = models.BooleanField(default=False)
    study_streak_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # Login with email instead of username, while still keeping username
    # around (required by AbstractUser / admin internals).
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
