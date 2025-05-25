from rest_framework.generics import ListAPIView

from .models import AnalysisResult
from .serializers import AnalysisResultSerializer


class AnalysisResultListView(ListAPIView):
    """Returns the list of my objects"""

    serializer_class = AnalysisResultSerializer
    queryset = AnalysisResult.objects.all()
