from django import forms
from .models import StudyPreference


class StudyPreferenceForm(forms.ModelForm):
    class Meta:
        model = StudyPreference
        fields = ["daily_available_hours", "preferred_start_time", "break_duration_minutes", "long_session_minutes"]
        widgets = {
            "daily_available_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.5", "min": "1", "max": "16"}),
            "preferred_start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "break_duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": "5", "max": "60"}),
            "long_session_minutes": forms.NumberInput(attrs={"class": "form-control", "min": "30", "max": "180"}),
        }
