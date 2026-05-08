from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TestResult


@login_required
def result_history(request):
    """Lists previous results for the logged-in student."""

    results = TestResult.objects.filter(student=request.user).select_related("semester", "subject")
    return render(request, "results/history.html", {"results": results})
