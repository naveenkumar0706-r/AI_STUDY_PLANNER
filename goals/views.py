from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Goal
from .forms import GoalForm


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class GoalListView(UserOwnedQuerysetMixin, ListView):
    model = Goal
    template_name = "goals/goal_list.html"
    context_object_name = "goals"
    paginate_by = 10


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = "goals/goal_form.html"
    success_url = reverse_lazy("goals:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"Goal '{form.instance.title}' created.")
        return super().form_valid(form)


class GoalUpdateView(UserOwnedQuerysetMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = "goals/goal_form.html"
    success_url = reverse_lazy("goals:list")

    def form_valid(self, form):
        messages.success(self.request, f"Goal '{form.instance.title}' updated.")
        return super().form_valid(form)


class GoalDeleteView(UserOwnedQuerysetMixin, DeleteView):
    model = Goal
    template_name = "goals/goal_confirm_delete.html"
    success_url = reverse_lazy("goals:list")

    def form_valid(self, form):
        messages.success(self.request, "Goal deleted.")
        return super().form_valid(form)
