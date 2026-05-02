from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_semester, name='select_semester'),
    path('subject/', views.select_subject, name='select_subject'),
    path('paper/', views.generate_paper, name='generate_paper'),
    path('upload/', views.upload_questions, name='upload_questions'),
]