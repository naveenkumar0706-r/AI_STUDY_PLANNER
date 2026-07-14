from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from subjects.models import Subject


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
