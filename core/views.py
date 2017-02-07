# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import api_view, parser_classes, permission_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from constance import config

from core import models as core_models
from core import serializers as core_serializers
from core.services import payutc

from picsous.permissions import IsAuthorizedUser, IsAdmin
from picsous.settings import CONSTANCE_CONFIG
from utcaccounts.utils import get_ginger_info


class BugReportViewset(viewsets.ModelViewSet):
    """
    BugReport viewset
    """
    permission_classes = (IsAuthorizedUser, )
    queryset = core_models.BugReport.objects.all()
    serializer_class = core_serializers.BugReportSerializer


class PeriodeTVAViewset(viewsets.ModelViewSet):
    """
    PeriodeTVA endpoint
    """
    permission_classes = (IsAdmin, )
    queryset = core_models.PeriodeTVA.objects.all()
    serializer_class = core_serializers.PeriodeTVASerializer


class SemestreViewset(viewsets.ModelViewSet):
    """
    Semestre endpoint
    """
    permission_classes = (IsAdmin, )
    queryset = core_models.Semestre.objects.all()
    serializer_class = core_serializers.SemestreSerializer


class UserRightViewset(viewsets.ModelViewSet):
    """
    UserRight endpoint
    """
    permission_classes = (IsAdmin, )
    queryset = core_models.UserRight.objects.all()
    serializer_class = core_serializers.UserRightSerializer


@api_view(['GET'])
@permission_classes((IsAuthorizedUser, ))
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

    return Response(c.call('USERRIGHT', 'userAutocomplete', queryString=query))


@api_view(['GET'])
@permission_classes((IsAdmin, ))
@renderer_classes((JSONRenderer, ))
def semestre_state(request):
    """
    Endpoint qui renvoie la somme des factures payées du semestre (émises et reçues)
    """
    return Response(core_models.Semestre.objects.get(pk=config.SEMESTER).get_paid_bills())


@api_view(['GET', 'PUT'])
@permission_classes((IsAdmin, ))
@parser_classes((JSONParser, ))
@renderer_classes((JSONRenderer, ))
def semester_beginning_credit(request):
    """
    Endpoint qui renvoie le solde au début du semestre actuel - sauf si 
    l'utilisateur spécifie un semester (avec le paramètre GET "semester")
    """
    semesterId = request.GET.get("semester", config.SEMESTER)
    semester = core_models.Semestre.objects.get(pk=semesterId)
    if request.method == 'PUT':
        semester.solde_debut = request.data['solde_debut']
        semester.save()
    return Response(int(semester.solde_debut))


def get_constance_params():
    return [{'key': key, 'value': config.__getattr__(key)} for key in CONSTANCE_CONFIG.keys()]


@api_view(['GET'])
@permission_classes((IsAdmin, ))
@renderer_classes((JSONRenderer, ))
def get_admin_settings(request):
    """
    Endpoint qui permet d'obtenir tous les paramètres de configuration de Picsous.
    """
    return Response(get_constance_params())


@api_view(['POST'])
@permission_classes((IsAdmin, ))
@parser_classes((JSONParser, ))
@renderer_classes((JSONRenderer, ))
def save_admin_settings(request):
    """
    Endpoint qui permet de sauvegarder les paramètres de configuration
    """
    for param in request.data:
        config.__setattr__(param['name'], param['val'])
    return Response(get_constance_params())


@api_view(['GET'])
@permission_classes((IsAdmin, ))
@parser_classes((JSONParser, ))
@renderer_classes((JSONRenderer, ))
def get_badge(request):
    """
    Endpoint qui permet d'obtenir un badge à partir d'un login
    """
    ginger_info = get_ginger_info(request.GET['login'])
    return Response(ginger_info['badge_uid'])
