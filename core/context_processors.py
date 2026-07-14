"""
Global context processor — makes lightweight stats available to every
template (navbar badges, sidebar counters) without every view having to
compute and pass them manually.
"""

from django.utils import timezone


def global_stats(request):
    if not request.user.is_authenticated:
        return {}

    from subjects.models import Subject
    from tasks.models import Task

    today = timezone.localdate()
    pending_tasks_today = Task.objects.filter(
        user=request.user, date=today, status="pending"
    ).count()

    return {
        "nav_subject_count": Subject.objects.filter(user=request.user).count(),
        "nav_pending_today": pending_tasks_today,
    }
