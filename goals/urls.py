from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [
    path("", views.GoalListView.as_view(), name="list"),
    path("add/", views.GoalCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.GoalUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.GoalDeleteView.as_view(), name="delete"),
]
