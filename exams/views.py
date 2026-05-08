from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from results.models import TestAnswer, TestResult

from .models import Question, Semester, Subject


PASS_PERCENTAGE = Decimal("40.00")


def home_page(request):
    """Shows the modern landing page and a quick semester overview."""

    # Count related subjects/questions so cards can show useful information.
    all_semesters = Semester.objects.annotate(
        subject_count=Count("subjects", distinct=True),
        question_count=Count("questions", distinct=True),
    )
    return render(request, "exams/home.html", {"semesters": all_semesters})


def select_semester(request):
    """Lets students choose the semester before choosing a subject."""

    # This page is separate from the home page to keep the test flow clear.
    all_semesters = Semester.objects.annotate(
        subject_count=Count("subjects", distinct=True),
        question_count=Count("questions", distinct=True),
    )
    return render(request, "exams/select_semester.html", {"semesters": all_semesters})


def select_subject(request, semester_id):
    """Shows subjects that belong to the selected semester."""

    # get_object_or_404 shows a normal 404 page if someone changes the URL manually.
    selected_semester = get_object_or_404(Semester, id=semester_id)
    subjects_for_semester = selected_semester.subjects.annotate(question_count=Count("questions"))
    return render(
        request,
        "exams/select_subject.html",
        {"semester": selected_semester, "subjects": subjects_for_semester},
    )


def start_test(request, semester_id, subject_id):
    """Shows all MCQs for the selected subject on one interactive test page."""

    selected_subject = get_object_or_404(Subject, id=subject_id, semester_id=semester_id)
    # order_by("?") randomizes question order every time the test opens.
    test_questions = Question.objects.filter(subject=selected_subject).order_by("?")

    if not test_questions.exists():
        messages.warning(request, "No questions are available for this subject yet.")
        return redirect("select_subject", semester_id=semester_id)

    return render(
        request,
        "exams/start_test.html",
        {
            "semester": selected_subject.semester,
            "subject": selected_subject,
            "questions": test_questions,
            "total_questions": test_questions.count(),
            "timer_minutes": 20,
        },
    )


def submit_test(request, semester_id, subject_id):
    """Checks submitted answers, saves the result, and redirects to the result page."""

    if request.method != "POST":
        return redirect("start_test", semester_id=semester_id, subject_id=subject_id)

    selected_subject = get_object_or_404(Subject, id=subject_id, semester_id=semester_id)
    test_questions = list(Question.objects.filter(subject=selected_subject))

    if not test_questions:
        messages.warning(request, "This test has no questions to submit.")
        return redirect("select_subject", semester_id=semester_id)

    selected_answers = {}
    for question in test_questions:
        # Radio inputs are named question_ID in the template, so we read them the same way.
        answer = request.POST.get(f"question_{question.id}")
        if not answer:
            messages.error(request, "Please answer every question before submitting.")
            return redirect("start_test", semester_id=semester_id, subject_id=subject_id)
        selected_answers[question.id] = answer

    correct_count = 0
    answer_rows = []
    for question in test_questions:
        # Compare the selected option with the correct option stored in the Question model.
        selected_answer = selected_answers[question.id]
        is_correct = selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1
        answer_rows.append(
            TestAnswer(
                question=question,
                selected_answer=selected_answer,
                correct_answer=question.correct_answer,
                is_correct=is_correct,
            )
        )

    total_questions = len(test_questions)
    wrong_count = total_questions - correct_count
    # Convert score into a percentage and keep two decimal places for display.
    percentage = (Decimal(correct_count) / Decimal(total_questions) * Decimal("100")).quantize(Decimal("0.01"))

    result = TestResult.objects.create(
        student=request.user if request.user.is_authenticated else None,
        semester=selected_subject.semester,
        subject=selected_subject,
        total_questions=total_questions,
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        percentage=percentage,
        passed=percentage >= PASS_PERCENTAGE,
    )

    # Attach each answer to the saved result so mistakes can be reviewed later.
    for answer_row in answer_rows:
        answer_row.result = result
    TestAnswer.objects.bulk_create(answer_rows)

    return redirect("show_result", result_id=result.id)


def show_result(request, result_id):
    """Displays score details and highlights correct/wrong answers."""

    result = get_object_or_404(
        TestResult.objects.select_related("semester", "subject").prefetch_related("answers__question"),
        id=result_id,
    )
    answer_details = []
    for answer in result.answers.all():
        # Convert answer letters like A/B/C/D into their option text for the review page.
        answer_details.append(
            {
                "answer": answer,
                "selected_text": answer.question.get_option_text(answer.selected_answer),
                "correct_text": answer.question.get_option_text(answer.correct_answer),
            }
        )
    message = "Excellent work. Keep practising to stay sharp." if result.passed else "Do not stop here. Revise and retake the test."
    return render(request, "results/show_result.html", {"result": result, "message": message, "answer_details": answer_details})


@staff_member_required
def admin_dashboard(request):
    """A simple custom admin dashboard for quick project overview."""

    # The custom dashboard is only a summary; detailed editing still happens in Django admin.
    recent_results = TestResult.objects.select_related("semester", "subject", "student")[:8]
    context = {
        "semester_count": Semester.objects.count(),
        "subject_count": Subject.objects.count(),
        "question_count": Question.objects.count(),
        "result_count": TestResult.objects.count(),
        "recent_results": recent_results,
    }
    return render(request, "exams/admin_dashboard.html", context)
