from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from results.models import TestResult

from .forms import StudentRegistrationForm


def register_student(request):
    """Shows the registration form and creates a new student account."""

    # Already logged-in students should not register again.
    if request.user.is_authenticated:
        return redirect("student_dashboard")

    # The same form handles blank display and submitted POST data.
    registration_form = StudentRegistrationForm(request.POST or None)

    if request.method == "POST" and registration_form.is_valid():
        # Save the new user, log them in, then send them to their dashboard.
        new_student = registration_form.save()
        login(request, new_student)
        return redirect("student_dashboard")

    return render(request, "accounts/register.html", {"form": registration_form})


class StudentLoginView(LoginView):
    """Shows the login page using Django's built-in LoginView."""

    template_name = "accounts/login.html"


class StudentLogoutView(LogoutView):
    """Logs out the student and returns to the home page."""

    next_page = "home_page"


@login_required
def student_dashboard(request):
    """Shows all test results submitted by the logged-in student."""

    # Filter results by current user so students only see their own attempts.
    student_results = TestResult.objects.filter(student=request.user).select_related("semester", "subject")
    return render(request, "accounts/dashboard.html", {"results": student_results})
