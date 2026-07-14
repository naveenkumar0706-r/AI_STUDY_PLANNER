import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone

from subjects.models import Subject
from tasks.models import Task
from goals.models import Goal
from exams.models import Exam
from planner.ai_engine import get_recommendations


def home_view(request):
    return render(request, "core/home.html")


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        if name and email and message:
            # In production: send an email / save a ContactMessage model.
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, "core/contact.html")


@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())

    subjects = Subject.objects.filter(user=user)
    tasks = Task.objects.filter(user=user)

    total_subjects = subjects.count()
    completed_tasks = tasks.filter(status="completed").count()
    pending_tasks = tasks.filter(status="pending").count()
    total_tasks = tasks.count()

    todays_study_hours = tasks.filter(date=today, status="completed").aggregate(
        total=Sum("estimated_hours")
    )["total"] or 0

    week_tasks = tasks.filter(date__gte=week_start, date__lte=today)
    weekly_completed = week_tasks.filter(status="completed").count()
    weekly_total = week_tasks.count()
    weekly_progress_pct = round((weekly_completed / weekly_total) * 100) if weekly_total else 0

    completion_percentage = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    # ---- Chart data -------------------------------------------------
    # Study Hours Chart: hours studied per day for the last 7 days
    study_hours_labels, study_hours_data = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        hours = tasks.filter(date=day, status="completed").aggregate(total=Sum("estimated_hours"))["total"] or 0
        study_hours_labels.append(day.strftime("%a"))
        study_hours_data.append(float(hours))

    # Weekly Performance: completed vs pending per day, last 7 days
    weekly_completed_data, weekly_pending_data = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        weekly_completed_data.append(tasks.filter(date=day, status="completed").count())
        weekly_pending_data.append(tasks.filter(date=day, status="pending").count())

    # Subject-wise progress
    subject_labels = [s.name for s in subjects]
    subject_progress = [s.completion_percentage for s in subjects]

    context = {
        "total_subjects": total_subjects,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "todays_study_hours": todays_study_hours,
        "weekly_progress_pct": weekly_progress_pct,
        "completion_percentage": completion_percentage,

        "chart_study_hours_labels": json.dumps(study_hours_labels),
        "chart_study_hours_data": json.dumps(study_hours_data),
        "chart_weekly_completed": json.dumps(weekly_completed_data),
        "chart_weekly_pending": json.dumps(weekly_pending_data),
        "chart_subject_labels": json.dumps(subject_labels),
        "chart_subject_progress": json.dumps(subject_progress),

        "recommendations": get_recommendations(user),
        "upcoming_exams": Exam.objects.filter(user=user, exam_date__gte=today).order_by("exam_date")[:3],
        "active_goals": Goal.objects.filter(user=user, is_completed=False).order_by("-created_at")[:3],
        "recent_tasks": tasks.order_by("-date", "-start_time")[:5],
    }
    return render(request, "core/dashboard.html", context)


@login_required
def search_view(request):
    """Unified search across Subjects, Tasks (Notes module can be added later)."""
    query = request.GET.get("q", "").strip()
    subjects, tasks = [], []
    if query:
        subjects = Subject.objects.filter(user=request.user, name__icontains=query)
        tasks = Task.objects.filter(user=request.user).filter(
            Q(title__icontains=query) | Q(notes__icontains=query)
        )
    return render(request, "core/search_results.html", {
        "query": query, "subjects": subjects, "tasks": tasks,
    })
