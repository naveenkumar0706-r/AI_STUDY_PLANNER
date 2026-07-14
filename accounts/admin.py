from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin panel view for Users, extending Django's default UserAdmin so
    password hashing / permission widgets keep working, while surfacing
    the extra study-planner profile fields in list view and fieldsets.
    """
    list_display = ("username", "email", "first_name", "college", "department", "year", "is_staff", "date_joined")
    list_filter = ("year", "department", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "college")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Study Planner Profile", {
            "fields": ("college", "department", "year", "mobile_number", "profile_picture",
                       "dark_mode_enabled", "study_streak_days"),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Study Planner Profile", {
            "fields": ("email", "college", "department", "year", "mobile_number"),
        }),
    )
