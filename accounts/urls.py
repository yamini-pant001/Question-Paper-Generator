from django.urls import path

from .views import StudentLoginView, StudentLogoutView, register_student, student_dashboard


# Account URLs are kept separate from exam URLs for easy understanding.
urlpatterns = [
    path("register/", register_student, name="register_page"),
    path("login/", StudentLoginView.as_view(), name="login"),
    path("logout/", StudentLogoutView.as_view(), name="logout"),
    path("dashboard/", student_dashboard, name="student_dashboard"),
]
