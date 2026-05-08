import django.conf
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(django.conf.settings.AUTH_USER_MODEL),
        ("exams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveIntegerField()),
                ("total_questions", models.PositiveIntegerField()),
                ("percentage", models.DecimalField(decimal_places=2, max_digits=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("semester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="test_attempts", to="exams.semester")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="test_attempts", to=django.conf.settings.AUTH_USER_MODEL)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="test_attempts", to="exams.subject")),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="StudentAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("selected_answer", models.CharField(max_length=1)),
                ("correct_answer", models.CharField(max_length=1)),
                ("is_correct", models.BooleanField(default=False)),
                ("attempt", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="results.testattempt")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="student_answers", to="exams.question")),
            ],
            options={"ordering": ("id",)},
        ),
    ]
