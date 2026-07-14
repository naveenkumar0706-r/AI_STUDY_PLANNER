from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .ai_engine import generate_daily_plan, get_recommendations, _get_or_create_preference
from .forms import StudyPreferenceForm
from .models import GeneratedPlanSlot


@login_required
def today_plan_view(request):
    """
    Displays today's AI-generated study plan. If no plan has been
    generated yet for today, generate one automatically so the page is
    never empty for a first-time visitor.
    """
    today = timezone.localdate()
    slots = GeneratedPlanSlot.objects.filter(user=request.user, date=today).select_related("subject")

    if not slots.exists():
        generate_daily_plan(request.user, target_date=today)
        slots = GeneratedPlanSlot.objects.filter(user=request.user, date=today).select_related("subject")

    context = {
        "slots": slots,
        "recommendations": get_recommendations(request.user),
        "today": today,
    }
    return render(request, "planner/today_plan.html", context)


@login_required
def regenerate_plan_view(request):
    """Force-regenerate today's plan (e.g. after adding/editing subjects)."""
    today = timezone.localdate()
    generate_daily_plan(request.user, target_date=today)
    messages.success(request, "Your AI study plan has been regenerated.")
    return redirect("planner:today")


@login_required
def preferences_view(request):
    pref = _get_or_create_preference(request.user)
    if request.method == "POST":
        form = StudyPreferenceForm(request.POST, instance=pref)
        if form.is_valid():
            form.save()
            messages.success(request, "Study preferences updated. Regenerate your plan to see the changes.")
            return redirect("planner:preferences")
    else:
        form = StudyPreferenceForm(instance=pref)

    return render(request, "planner/preferences.html", {"form": form})
