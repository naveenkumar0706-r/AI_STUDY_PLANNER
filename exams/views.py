from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Exam
from .forms import ExamForm


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ExamListView(UserOwnedQuerysetMixin, ListView):
    model = Exam
    template_name = "exams/exam_list.html"
    context_object_name = "exams"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related("subject")


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = "exams/exam_form.html"
    success_url = reverse_lazy("exams:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"Exam '{form.instance.exam_name}' added.")
        return super().form_valid(form)


class ExamUpdateView(UserOwnedQuerysetMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = "exams/exam_form.html"
    success_url = reverse_lazy("exams:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f"Exam '{form.instance.exam_name}' updated.")
        return super().form_valid(form)


class ExamDeleteView(UserOwnedQuerysetMixin, DeleteView):
    model = Exam
    template_name = "exams/exam_confirm_delete.html"
    success_url = reverse_lazy("exams:list")

    def form_valid(self, form):
        messages.success(self.request, "Exam deleted.")
        return super().form_valid(form)
