from django import forms
from .models import Task
from subjects.models import Subject


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "date", "start_time", "end_time", "estimated_hours", "status", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Revise Chapter 3"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "estimated_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.5", "min": "0.5"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["subject"].queryset = Subject.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data
