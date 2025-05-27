from django.urls import path

from .views import AnalysisResultListView, AnalysisResultDetailView

app_name = "analytics"

urlpatterns = [
    path("", AnalysisResultListView.as_view()),
    path("<int:id>/", AnalysisResultDetailView.as_view()),
]
