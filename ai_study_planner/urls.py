"""
Root URL configuration for ai_study_planner project.
Each app owns its own urls.py, included here with a namespace.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("subjects/", include("subjects.urls", namespace="subjects")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("exams/", include("exams.urls", namespace="exams")),
    path("goals/", include("goals.urls", namespace="goals")),
    path("planner/", include("planner.urls", namespace="planner")),
]

# Serve user-uploaded media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
