from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "difficulty_level", "priority", "credits", "target_score", "created_at")
    list_filter = ("difficulty_level", "priority")
    search_fields = ("name", "user__email")
