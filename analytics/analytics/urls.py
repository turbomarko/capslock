from django.urls import path

from .views import AnalysisResultListView

app_name = "analytics"

urlpatterns = [
    path("", AnalysisResultListView.as_view()),
]
