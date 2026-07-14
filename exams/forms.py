from django import forms
from .models import Exam
from subjects.models import Subject


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["exam_name", "subject", "exam_date", "preparation_level"]
        widgets = {
            "exam_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mid-Semester Exam"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "exam_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "preparation_level": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["subject"].queryset = Subject.objects.filter(user=user)
