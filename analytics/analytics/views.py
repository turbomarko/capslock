from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import AnalysisResult
from .serializers import AnalysisResultSerializer, AnalysisResultListSerializer


class AnalysisResultListView(ListAPIView):
    """Returns the list of analysis results with filtering capabilities"""

    serializer_class = AnalysisResultListSerializer

    def get_queryset(self):
        queryset = AnalysisResult.objects.all()
        
        # Get query parameters
        severity = self.request.query_params.get('severity')
        analysis_type = self.request.query_params.get('analysisType')
        metric_affected = self.request.query_params.get('metricAffected')
        date_start = self.request.query_params.get('dateRange.start')
        date_end = self.request.query_params.get('dateRange.end')
        
        # Apply filters
        if severity:
            queryset = queryset.filter(severity=severity)
        if analysis_type:
            queryset = queryset.filter(analysis_type=analysis_type)
        if metric_affected:
            queryset = queryset.filter(metric_affected=metric_affected)
        if date_start:
            queryset = queryset.filter(date_detected__gte=date_start)
        if date_end:
            queryset = queryset.filter(date_detected__lte=date_end)
            
        return queryset.order_by('-date_detected')


class AnalysisResultDetailView(RetrieveAPIView):
    """Returns a single analysis result by ID"""
    serializer_class = AnalysisResultSerializer
    queryset = AnalysisResult.objects.all()
    lookup_field = 'id'
