from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200, help_text="e.g. Complete Python in 10 Days")
    target_date = models.DateField(null=True, blank=True)
    total_units = models.PositiveIntegerField(default=100, help_text="Total steps/units to reach 100%")
    completed_units = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def percentage(self):
        if self.total_units == 0:
            return 0
        pct = round((self.completed_units / self.total_units) * 100)
        return min(pct, 100)

    @property
    def remaining_units(self):
        return max(self.total_units - self.completed_units, 0)

    def save(self, *args, **kwargs):
        # Auto-flag completion once units reach the target.
        self.is_completed = self.completed_units >= self.total_units
        super().save(*args, **kwargs)
