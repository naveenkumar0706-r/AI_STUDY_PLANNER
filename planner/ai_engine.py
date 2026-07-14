"""
Rule-based AI Recommendation Engine
====================================

This module is the "AI" in AI Study Planner. It's deliberately built as a
transparent, explainable rule-based scoring system rather than a black-box
ML model — every recommendation can be traced back to a reason, which
matters for a study tool students actually need to trust.

The design is intentionally modular so it can be upgraded later: swap
`compute_subject_scores()` for a trained model that predicts an
"attention score" per subject, and everything downstream (daily plan
generation, recommendations) keeps working unchanged.

Scoring factors (rule-based):
    1. Priority          -> subject.priority (Low/Medium/High)
    2. Difficulty         -> harder subjects get more time
    3. Exam urgency        -> closer exam date = higher urgency boost
    4. Completion rate     -> subjects the student is behind on get boosted
    5. Target score gap    -> ambitious target scores get a small boost

The output is a ranked list of subjects with numeric scores and
human-readable reasons, which is then used to:
    - allocate the day's available study hours proportionally
    - build a literal time-blocked schedule with breaks
    - power the "AI Recommendation Engine" widgets on the dashboard
"""

import random
from datetime import datetime, timedelta, date as date_cls
from decimal import Decimal

from django.utils import timezone

from subjects.models import Subject
from tasks.models import Task
from exams.models import Exam
from .models import StudyPreference, GeneratedPlanSlot


DIFFICULTY_WEIGHT = {"easy": 5, "medium": 10, "hard": 15}
PRIORITY_WEIGHT = {1: 5, 2: 10, 3: 18}  # Low, Medium, High

MOTIVATIONAL_QUOTES = [
    "Success is the sum of small efforts repeated day in and day out.",
    "The secret of getting ahead is getting started.",
    "Don't watch the clock; do what it does. Keep going.",
    "Discipline is choosing between what you want now and what you want most.",
    "Small daily improvements are the key to staggering long-term results.",
    "You don't have to be great to start, but you have to start to be great.",
    "Focus on progress, not perfection.",
    "Every hour of focused study is a deposit into your future.",
]

STUDY_TIPS = [
    "Use the Pomodoro technique: 25 minutes focused, 5 minutes break.",
    "Teach a concept out loud to someone (or yourself) to test real understanding.",
    "Review yesterday's notes for 5 minutes before starting new material.",
    "Tackle your hardest subject when your energy is highest, usually mornings.",
    "Sleep is part of studying — memory consolidates during rest.",
    "Space out revision instead of cramming; spaced repetition beats marathon sessions.",
    "Turn off notifications during study blocks to protect deep focus.",
]


def _get_or_create_preference(user):
    pref, _ = StudyPreference.objects.get_or_create(user=user)
    return pref


def _subject_completion_rate(subject):
    """Historical completion rate for a subject, used to detect weak spots."""
    total = subject.tasks.count()
    if total == 0:
        return None  # no history yet — treat neutrally
    completed = subject.tasks.filter(status="completed").count()
    return completed / total


def _days_until_next_exam(subject):
    upcoming = (
        Exam.objects.filter(subject=subject, exam_date__gte=date_cls.today())
        .order_by("exam_date")
        .first()
    )
    if not upcoming:
        return None
    return max(upcoming.days_remaining, 0)


def compute_subject_scores(user):
    """
    Returns a list of dicts, one per subject, each with a numeric `score`
    and a list of human-readable `reasons` explaining the score — sorted
    highest score (most urgent/important) first.
    """
    results = []
    subjects = Subject.objects.filter(user=user)

    for subject in subjects:
        score = 0.0
        reasons = []

        # 1. Priority
        priority_pts = PRIORITY_WEIGHT.get(subject.priority, 10)
        score += priority_pts
        if subject.priority == 3:
            reasons.append("High priority subject")

        # 2. Difficulty
        difficulty_pts = DIFFICULTY_WEIGHT.get(subject.difficulty_level, 10)
        score += difficulty_pts
        if subject.difficulty_level == "hard":
            reasons.append("Marked as a hard subject")

        # 3. Exam urgency — the closer the exam, the bigger the boost.
        days_left = _days_until_next_exam(subject)
        if days_left is not None:
            if days_left <= 3:
                score += 30
                reasons.append(f"Exam in {days_left} day(s) — urgent")
            elif days_left <= 7:
                score += 20
                reasons.append(f"Exam in {days_left} days — coming up soon")
            elif days_left <= 14:
                score += 10
                reasons.append(f"Exam in {days_left} days")

        # 4. Completion rate — behind schedule = weak subject = boost.
        completion_rate = _subject_completion_rate(subject)
        if completion_rate is not None:
            if completion_rate < 0.4:
                score += 20
                reasons.append("Low task completion rate — needs attention")
            elif completion_rate < 0.7:
                score += 10
                reasons.append("Moderate completion rate")
        else:
            reasons.append("No task history yet")

        # 5. Ambitious target score gets a small nudge.
        if subject.target_score >= 90:
            score += 5
            reasons.append("Ambitious target score")

        results.append({
            "subject": subject,
            "score": round(score, 1),
            "reasons": reasons,
            "completion_rate": completion_rate,
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def get_weak_subjects(user, threshold=0.4):
    """Subjects whose completion rate is below the threshold."""
    weak = []
    for row in compute_subject_scores(user):
        rate = row["completion_rate"]
        if rate is not None and rate < threshold:
            weak.append(row["subject"])
    return weak


def get_high_priority_subjects(user):
    return [row["subject"] for row in compute_subject_scores(user) if row["subject"].priority == 3]


def recommended_daily_hours(user):
    """
    Suggests total daily study hours based on subject load and how many
    exams are coming up in the next 14 days — capped to something humane.
    """
    subjects_count = Subject.objects.filter(user=user).count()
    upcoming_exams = Exam.objects.filter(
        user=user, exam_date__gte=date_cls.today(), exam_date__lte=date_cls.today() + timedelta(days=14)
    ).count()

    base = 2 + min(subjects_count, 6) * 0.5
    base += upcoming_exams * 0.75
    return round(min(base, 10), 1)  # never recommend more than 10 hrs/day


def get_recommendations(user):
    """
    Aggregates everything the 'AI Recommendation Engine' section of the
    dashboard needs into one call.
    """
    scores = compute_subject_scores(user)
    return {
        "high_priority_subjects": [r["subject"] for r in scores if r["subject"].priority == 3][:3],
        "weak_subjects": get_weak_subjects(user)[:3],
        "revision_schedule": [r["subject"] for r in scores if r["score"] >= 25][:3],
        "daily_quote": random.choice(MOTIVATIONAL_QUOTES),
        "study_tip": random.choice(STUDY_TIPS),
        "recommended_hours": recommended_daily_hours(user),
        "scored_subjects": scores,
    }


def generate_daily_plan(user, target_date=None, persist=True):
    """
    Builds a literal time-blocked study plan for `target_date` (default:
    today), allocating the user's available hours across subjects
    proportionally to their urgency score, and inserting breaks after
    every `long_session_minutes` of continuous study.

    Returns a list of dicts: {start_time, end_time, type, label, reason}
    and optionally persists them as GeneratedPlanSlot rows (clearing any
    previous plan for that date first, so re-generating is idempotent).
    """
    target_date = target_date or timezone.localdate()
    pref = _get_or_create_preference(user)
    scores = compute_subject_scores(user)

    if not scores:
        return []

    total_minutes = int(Decimal(pref.daily_available_hours) * 60)
    total_score = sum(r["score"] for r in scores) or 1

    # Allocate minutes proportional to score, with a sensible floor/ceiling
    # per subject so no subject gets 0 minutes or hogs the whole day.
    allocations = []
    for row in scores:
        share = row["score"] / total_score
        minutes = int(total_minutes * share)
        minutes = max(minutes, 20)          # floor: at least 20 min if it made the list
        minutes = min(minutes, 150)          # ceiling: no more than 2.5 hrs in one go
        allocations.append({"subject": row["subject"], "minutes": minutes, "reasons": row["reasons"]})

    # Trim total back down to the available budget if we overshot due to floors.
    allocated_total = sum(a["minutes"] for a in allocations)
    if allocated_total > total_minutes:
        scale = total_minutes / allocated_total
        for a in allocations:
            a["minutes"] = max(int(a["minutes"] * scale), 15)

    # Walk through allocations, laying out real clock times with breaks.
    slots = []
    current_dt = datetime.combine(target_date, pref.preferred_start_time)
    continuous_minutes = 0

    for alloc in allocations:
        minutes_left = alloc["minutes"]
        while minutes_left > 0:
            chunk = min(minutes_left, pref.long_session_minutes - continuous_minutes)
            chunk = max(chunk, 0)
            if chunk == 0:
                # insert a break, then continue this subject's remaining time
                break_end = current_dt + timedelta(minutes=pref.break_duration_minutes)
                slots.append({
                    "start_time": current_dt.time(),
                    "end_time": break_end.time(),
                    "type": "break",
                    "subject": None,
                    "label": "Break",
                    "reason": "Recovery break to maintain focus",
                })
                current_dt = break_end
                continuous_minutes = 0
                continue

            slot_end = current_dt + timedelta(minutes=chunk)
            slots.append({
                "start_time": current_dt.time(),
                "end_time": slot_end.time(),
                "type": "study",
                "subject": alloc["subject"],
                "label": alloc["subject"].name,
                "reason": "; ".join(alloc["reasons"]) or "Scheduled study block",
            })
            current_dt = slot_end
            continuous_minutes += chunk
            minutes_left -= chunk

    # Always close the day with a short revision block on the top-scoring subject.
    top_subject = scores[0]["subject"]
    revision_end = current_dt + timedelta(minutes=30)
    slots.append({
        "start_time": current_dt.time(),
        "end_time": revision_end.time(),
        "type": "revision",
        "subject": top_subject,
        "label": f"Revision — {top_subject.name}",
        "reason": "End-of-day recall strengthens retention on your top-priority subject",
    })

    if persist:
        GeneratedPlanSlot.objects.filter(user=user, date=target_date).delete()
        GeneratedPlanSlot.objects.bulk_create([
            GeneratedPlanSlot(
                user=user,
                subject=s["subject"],
                date=target_date,
                start_time=s["start_time"],
                end_time=s["end_time"],
                slot_type=s["type"],
                reason=s["reason"][:255],
            )
            for s in slots
        ])

    return slots
