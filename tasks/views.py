from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TaskListView(UserOwnedQuerysetMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("subject")
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")
        if query:
            qs = qs.filter(title__icontains=query)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = Task.STATUS_CHOICES
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"Task '{form.instance.title}' created.")
        return super().form_valid(form)


class TaskUpdateView(UserOwnedQuerysetMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f"Task '{form.instance.title}' updated.")
        return super().form_valid(form)


class TaskDeleteView(UserOwnedQuerysetMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)
