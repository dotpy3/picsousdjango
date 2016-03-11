from rest_framework import viewsets
from core import models as core_models
from core import serializers as core_serializers
from core.services import payutc


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


@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def autocomplete(request, query):
    c = payutc.Client()
    c.loginApp()
    c.loginBadge()

    return Response(c.call('TRESO', 'userAutocomplete', queryString=query))
