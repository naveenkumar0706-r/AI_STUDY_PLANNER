from django.conf import settings
from django.db import models

from subjects.models import Subject


class StudyPreference(models.Model):
    """
    One row per user. Feeds the AI engine's daily-hours ceiling and
    preferred start time so the generated plan matches real availability.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_preference")
    daily_available_hours = models.DecimalField(max_digits=4, decimal_places=1, default=6.0)
    preferred_start_time = models.TimeField(default="09:00")
    break_duration_minutes = models.PositiveSmallIntegerField(default=15)
    long_session_minutes = models.PositiveSmallIntegerField(
        default=90, help_text="Minutes of focused study before a break is inserted"
    )

    def __str__(self):
        return f"Study preferences for {self.user}"


class GeneratedPlanSlot(models.Model):
    """
    Persisted output of the AI recommendation engine for a given day, so
    the dashboard/calendar can render "today's plan" without recomputing
    it on every page load, and so history/analytics are possible later.
    """
    SLOT_TYPE_CHOICES = [
        ("study", "Study"),
        ("break", "Break"),
        ("revision", "Revision"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plan_slots")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="plan_slots", null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_type = models.CharField(max_length=10, choices=SLOT_TYPE_CHOICES, default="study")
    reason = models.CharField(max_length=255, blank=True, help_text="Why the AI engine chose this slot")

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        label = self.subject.name if self.subject else self.get_slot_type_display()
        return f"{self.date} {self.start_time}-{self.end_time}: {label}"
