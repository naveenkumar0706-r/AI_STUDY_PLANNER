from datetime import date

from django.conf import settings
from django.db import models

from subjects.models import Subject


class Exam(models.Model):
    PREPARATION_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("well_prepared", "Well Prepared"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exams")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exams")
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    preparation_level = models.CharField(max_length=15, choices=PREPARATION_CHOICES, default="not_started")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["exam_date"]

    def __str__(self):
        return f"{self.exam_name} - {self.subject.name}"

    @property
    def days_remaining(self):
        return (self.exam_date - date.today()).days
