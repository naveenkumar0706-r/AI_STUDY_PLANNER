from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Subject
from .forms import SubjectForm


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    """Ensures users can only ever see/edit/delete their own records."""

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SubjectListView(UserOwnedQuerysetMixin, ListView):
    model = Subject
    template_name = "subjects/subject_list.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(name__icontains=query)
        return qs


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"Subject '{form.instance.name}' added successfully.")
        return super().form_valid(form)


class SubjectUpdateView(UserOwnedQuerysetMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:list")

    def form_valid(self, form):
        messages.success(self.request, f"Subject '{form.instance.name}' updated successfully.")
        return super().form_valid(form)


class SubjectDeleteView(UserOwnedQuerysetMixin, DeleteView):
    model = Subject
    template_name = "subjects/subject_confirm_delete.html"
    success_url = reverse_lazy("subjects:list")

    def form_valid(self, form):
        messages.success(self.request, "Subject deleted.")
        return super().form_valid(form)
