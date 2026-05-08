import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Semester",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("semester_name", models.CharField(max_length=100, unique=True)),
            ],
            options={"ordering": ("semester_name",)},
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject_name", models.CharField(max_length=150)),
                ("semester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subjects", to="exams.semester")),
            ],
            options={
                "ordering": ("semester__semester_name", "subject_name"),
                "unique_together": {("subject_name", "semester")},
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_text", models.TextField()),
                ("option_a", models.CharField(max_length=255)),
                ("option_b", models.CharField(max_length=255)),
                ("option_c", models.CharField(max_length=255)),
                ("option_d", models.CharField(max_length=255)),
                ("correct_answer", models.CharField(choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("semester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="exams.semester")),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="exams.subject")),
            ],
            options={"ordering": ("semester__semester_name", "subject__subject_name", "id")},
        ),
    ]
