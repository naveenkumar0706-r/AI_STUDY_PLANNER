from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("today/", views.today_plan_view, name="today"),
    path("regenerate/", views.regenerate_plan_view, name="regenerate"),
    path("preferences/", views.preferences_view, name="preferences"),
]
