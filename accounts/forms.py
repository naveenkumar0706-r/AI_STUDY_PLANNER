from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class RegistrationForm(UserCreationForm):
    """
    Registration form covering all fields requested in the spec:
    Name, Email, Password, Confirm Password, College, Department, Year,
    Mobile Number. UserCreationForm already gives us password + confirm
    password validation for free.
    """

    first_name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "you@example.com"}))
    college = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "College name"}))
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "e.g. Computer Science"}))
    year = forms.ChoiceField(choices=User.YEAR_CHOICES, required=False,
                              widget=forms.Select(attrs={"class": "form-select"}))
    mobile_number = forms.CharField(max_length=17, required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "+91XXXXXXXXXX"}))

    class Meta:
        model = User
        fields = [
            "first_name", "email", "college", "department",
            "year", "mobile_number", "password1", "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm password"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # email doubles as username
        user.first_name = self.cleaned_data["first_name"]
        user.college = self.cleaned_data.get("college", "")
        user.department = self.cleaned_data.get("department", "")
        user.year = self.cleaned_data.get("year", "")
        user.mobile_number = self.cleaned_data.get("mobile_number", "")
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "you@example.com", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "college",
            "department", "year", "mobile_number", "profile_picture",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "college": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.Select(attrs={"class": "form-select"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
        }
