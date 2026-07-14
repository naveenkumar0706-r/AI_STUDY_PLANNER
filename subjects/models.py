from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    PRIORITY_CHOICES = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=150)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=2)
    credits = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(10)])
    target_score = models.PositiveSmallIntegerField(
        default=80, validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Target score out of 100"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "name"]
        unique_together = ("user", "name")

    def __str__(self):
        return self.name

    @property
    def completion_percentage(self):
        """Percentage of this subject's tasks that are completed."""
        total = self.tasks.count()
        if total == 0:
            return 0
        done = self.tasks.filter(status="completed").count()
        return round((done / total) * 100)
