from django.urls import path

from .views import result_history

urlpatterns = [
    path("history/", result_history, name="result_history"),
]
