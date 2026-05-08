from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationForm(UserCreationForm):
    """Simple registration form for students.

    This form uses Django's built-in User model, so we do not need to create
    a complicated custom user system for this beginner-friendly project.
    """

    class Meta:
        model = get_user_model()
        # username and password fields are enough for a small MCQ test portal.
        fields = ("username",)
