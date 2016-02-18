#-*- coding: utf-8 -*-

import json

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core import models as core_models
from core import serializers as core_serializers
from core.services import payutc

from picsous.settings import NEMOPAY_LOGIN_SERVICE

from settings import UTC_CAS_URL

from .utils import CASTicket, user_creation, nemopay_connection_active

def home_redirection():
    return redirect('payetonasso.views.home')

def dashboard_redirection():
    return redirect('payetonasso.views.dashboard')

def connexion_cas(request):
    if request.user.is_authenticated() and nemopay_connection_active(request):
        return dashboard_redirection()
    ticket = request.GET.get('ticket', '')
    if ticket is None or ticket == '':
        return redirect(UTC_CAS_URL + 'login/?service=' + request.build_absolute_uri())
    else:
        user_ticket = CASTicket(request.build_absolute_uri().split('?')[0], ticket)
        (login_given, sessionid) = user_ticket.get_information()
        login_given = login_given.lower()
        # at this point, login_given contains the CAS login
        user = authenticate(username=login_given)
        if user is None:
            user = user_creation(login_given)
        if user.is_active:
            user = authenticate(username=login_given)
            login(request, user)
        else:
            return redirect('payetonasso.home', { 'deactivated': True })
        response = dashboard_redirection()
        if sessionid is not None:
            response.set_cookie(key='nemopay_sessionid', value=sessionid)
        return response

def deconnexion(request):
    logout(request)
    return home_redirection()

connection_successful = {'success': {'login': None}}

def get_connection_successful(login):
    connection_successful['success']['login'] = login
    return Response(connection_successful)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def connexion_cas_api(request):
    if request.user.is_authenticated():
        return get_connection_successful(request.user.get_username())
    c = payutc.Client()
    content = json.loads(request.body)
    for i in ('ticket', 'service'):
        if i not in content.keys():
            content[i] = None
    sr = core_serializers.LoginInputSerializer(data={'ticket': content['ticket'], 'service': content['service']})
    sr.is_valid(raise_exception=True)
    data = sr.validated_data
    (login_given, _session_id) = c.loginCas(ticket=data['ticket'], service=data['service'])
    if 'Invalid credentials' in login_given:
        raise ValidationError('CAS login failed')
    user = authenticate(username=login_given)
    if user is None:
        if core_models.UserRight.objects.filter(login=login_given).exclude(right=core_models.UserRight.USERRIGHT_NONE).count():
            user = user_creation(login_given)
        else:
            raise PermissionDenied('User has no right')
    user.is_staff = core_models.UserRight.objects.filter(login=login_given, right=core_models.UserRight.USERRIGHT_ALL).count() > 0
    user.save()
    if user.is_active:
        user = authenticate(username=login_given)
        login(request, user)
    else:
        raise PermissionDenied('Account deactivated')
    return get_connection_successful(login_given)

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def get_my_rights(request):
    if not request.user.is_authenticated():
        return Response('NONE')
    ur = core_models.UserRight.objects.get(login=request.user.username)
    if ur.right == core_models.UserRight.USERRIGHT_ALL:
        return Response('ALL')
    else:
        return Response('ARTICLES')
