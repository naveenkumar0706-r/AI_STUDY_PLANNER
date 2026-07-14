from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "difficulty_level", "priority", "credits", "target_score"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mathematics"}),
            "difficulty_level": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "credits": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
            "target_score": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
        }
