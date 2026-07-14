from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "user", "date", "start_time", "end_time", "status")
    list_filter = ("status", "date")
    search_fields = ("title", "user__email", "subject__name")
    date_hierarchy = "date"
