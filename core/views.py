# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core import models as core_models
from core import serializers as core_serializers
from core.services import payutc


class BugReportViewset(viewsets.ModelViewSet):
    """
    BugReport viewset
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
    """
    Endpoint qui utilise la méthode userAutocomplete de PayUTC pour créer un
    autocomplete sur l'interface picsous.
    On envoit une querystring, le serveur se connecte et renvoie les résultats à
    l'utilisateur.
    
    XXX : la connexion à chaque fois prend trop de temps. Est-ce que ce ne serait pas
    possible d'optimiser, notamment par un session id, pour pas que le serveur réétablisse
    l'authentification à chaque fois ?
    """
    c = payutc.Client()
    c.loginApp()
    c.loginBadge()

    return Response(c.call('TRESO', 'userAutocomplete', queryString=query))
