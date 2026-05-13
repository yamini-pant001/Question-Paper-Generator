from django.contrib import admin

from .models import TestAnswer, TestResult


class TestAnswerInline(admin.TabularInline):
        """Shows submitted answers inside a result record."""

        model = TestAnswer
        extra = 0
        readonly_fields = ("question", "selected_answer", "correct_answer", "is_correct")
        can_delete = False


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
        """Admin view for checking student test performance."""

        list_display = ("subject", "semester", "student", "correct_answers", "total_questions", "percentage", "passed")
        list_filter = ("semester", "subject", "passed", "created_at")
        search_fields = ("subject__subject_name", "semester__semester_name", "student__username")
        readonly_fields = ("created_at",)
        inlines = (TestAnswerInline,)


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
        """Admin view for individual answer records."""

        list_display = ("question", "selected_answer", "correct_answer", "is_correct")
        list_filter = ("is_correct", "correct_answer")
        search_fields = ("question__question_text",)
