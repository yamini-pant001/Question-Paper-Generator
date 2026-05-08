from django.db import models


class Semester(models.Model):
    """Stores one semester, such as Semester 1 or Semester 2."""

    # semester_name clearly tells us this field stores the name of the semester.
    semester_name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("semester_name",)
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return self.semester_name


class Subject(models.Model):
    """Stores subjects under a semester so tests can be grouped clearly."""

    # Each subject belongs to exactly one semester.
    semester = models.ForeignKey(Semester, related_name="subjects", on_delete=models.CASCADE)
    # subject_name clearly tells us this field stores the name of the subject.
    subject_name = models.CharField(max_length=150)

    class Meta:
        ordering = ("semester__semester_name", "subject_name")
        unique_together = ("semester", "subject_name")
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.subject_name} ({self.semester.semester_name})"


class Question(models.Model):
    """Stores one MCQ question with four options and the correct answer."""

    ANSWER_CHOICES = (
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
        ("D", "Option D"),
    )

    # The semester is filled automatically from the selected subject in save().
    semester = models.ForeignKey(Semester, related_name="questions", on_delete=models.CASCADE, editable=False)
    # The selected subject decides where this question appears in the test flow.
    subject = models.ForeignKey(Subject, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()
    # Four separate fields make the MCQ options very clear in Django admin.
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    # Stores only A, B, C, or D instead of repeating the full option text.
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    class Meta:
        ordering = ("semester__semester_name", "subject__subject_name", "id")
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def save(self, *args, **kwargs):
        # A subject already belongs to a semester, so this keeps both fields matching.
        if self.subject_id:
            self.semester = self.subject.semester
        self.correct_answer = self.correct_answer.upper()
        super().save(*args, **kwargs)

    def get_option_text(self, option_key):
        """Returns the visible option text for A, B, C, or D."""

        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }.get(option_key, "")

    def __str__(self):
        return self.question_text[:80]
