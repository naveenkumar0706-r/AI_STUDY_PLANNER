from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "total_units", "completed_units", "is_completed", "target_date")
    list_filter = ("is_completed",)
    search_fields = ("title", "user__email")
