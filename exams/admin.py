from django.contrib import admin

from .models import Question, Semester, Subject


admin.site.site_header = "Interactive MCQ Test System"
admin.site.site_title = "MCQ Admin"
admin.site.index_title = "Manage semesters, subjects, and questions"


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    """Admin setup for adding and editing semesters."""

    list_display = ("semester_name",)
    search_fields = ("semester_name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin setup for adding subjects under a semester."""

    list_display = ("subject_name", "semester")
    list_filter = ("semester",)
    search_fields = ("subject_name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin setup for managing MCQ questions and correct answers."""

    list_display = ("question_text", "semester", "subject", "correct_answer")
    list_filter = ("semester", "subject", "correct_answer")
    search_fields = ("question_text", "option_a", "option_b", "option_c", "option_d")
    fieldsets = (
        ("Question Details", {"fields": ("subject", "question_text")}),
        ("Options", {"fields": ("option_a", "option_b", "option_c", "option_d")}),
        ("Answer", {"fields": ("correct_answer",)}),
    )
