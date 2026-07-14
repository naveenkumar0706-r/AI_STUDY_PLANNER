from django.contrib import admin
from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("exam_name", "subject", "user", "exam_date", "preparation_level")
    list_filter = ("preparation_level",)
    search_fields = ("exam_name", "user__email", "subject__name")
    date_hierarchy = "exam_date"
