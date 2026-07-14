from django.contrib import admin
from .models import StudyPreference, GeneratedPlanSlot


@admin.register(StudyPreference)
class StudyPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_available_hours", "preferred_start_time", "break_duration_minutes")


@admin.register(GeneratedPlanSlot)
class GeneratedPlanSlotAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "start_time", "end_time", "slot_type", "subject")
    list_filter = ("slot_type", "date")
    search_fields = ("user__email",)
