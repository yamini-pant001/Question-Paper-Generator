from django.conf import settings
from django.db import models

from exams.models import Question, Semester, Subject


class TestResult(models.Model):
    """Stores the final score for one submitted MCQ test."""

    # Student is optional so guests can also attempt tests.
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="test_results",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    semester = models.ForeignKey(Semester, related_name="test_results", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="test_results", on_delete=models.CASCADE)
    # These fields store the calculated score shown on the result page.
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    # passed is saved so the result page and admin dashboard do not recalculate it.
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"

    def __str__(self):
        return f"{self.subject.subject_name} - {self.percentage}%"


class TestAnswer(models.Model):
    """Stores each submitted answer so the result page can explain mistakes."""

    # One result has many saved answers, one for each question in that test.
    result = models.ForeignKey(TestResult, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="test_answers", on_delete=models.CASCADE)
    # selected_answer is the student's choice; correct_answer is copied for easy review.
    selected_answer = models.CharField(max_length=1)
    correct_answer = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ("id",)
        verbose_name = "Test Answer"
        verbose_name_plural = "Test Answers"

    def __str__(self):
        return f"Question {self.question_id}: {self.selected_answer}"
