from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "target_date", "total_units", "completed_units"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Complete Python in 10 Days"}),
            "target_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "total_units": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "completed_units": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }
