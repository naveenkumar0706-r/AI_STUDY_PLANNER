from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegistrationForm, LoginForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Welcome, {user.first_name}! Your account was created successfully.")
            login(request, user)
            return redirect("core:dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get("next", "core:dashboard")
                return redirect(next_url)
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. See you soon!")
    return redirect("core:home")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


# ---------------------------------------------------------------------
# Forgot Password — Django's built-in class-based views handle the token
# generation, email dispatch, and secure link validation. We just point
# them at our own templates and URL names.
# ---------------------------------------------------------------------
class StudyPlannerPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class StudyPlannerPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class StudyPlannerPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class StudyPlannerPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
