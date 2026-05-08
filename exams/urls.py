from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("semesters/", views.select_semester, name="select_semester"),
    path("semester/<int:semester_id>/subjects/", views.select_subject, name="select_subject"),
    path("semester/<int:semester_id>/subject/<int:subject_id>/test/", views.start_test, name="start_test"),
    path("semester/<int:semester_id>/subject/<int:subject_id>/submit/", views.submit_test, name="submit_test"),
    path("result/<int:result_id>/", views.show_result, name="show_result"),
    path("custom-admin/", views.admin_dashboard, name="admin_dashboard"),
]
