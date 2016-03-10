from rest_framework import viewsets
from core import models as core_models
from core import serializers as core_serializers


class BugReportViewset(viewsets.ModelViewSet):
    """
    BugReport endpoint
    """
    queryset = core_models.BugReport.objects.all()
    serializer_class = core_serializers.BugReportSerializer


class PeriodeTVAViewset(viewsets.ModelViewSet):
    """
    PeriodeTVA endpoint
    """
    queryset = core_models.PeriodeTVA.objects.all()
    serializer_class = core_serializers.PeriodeTVASerializer
