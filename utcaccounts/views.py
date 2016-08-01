# coding: utf-8

""" Vues du module de connexion """

import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core import models as core_models
from core import serializers as core_serializers
from core.services import payutc
from picsous.permissions import IsAdmin, IsAuthorizedUser
from utcaccounts.utils import user_creation

CONNECTION_SUCCESSFUL = {'success': {'login': None, 'token': None}}

def get_connection_successful(login_nick, token=None):
    """ Fonction de réponse de login réussi """
    CONNECTION_SUCCESSFUL['success']['login'] = login_nick
    if token:
        CONNECTION_SUCCESSFUL['success']['token'] = token.key
    return Response(CONNECTION_SUCCESSFUL)

@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def connexion_cas_api(request):
    """ Endpoint de connexion au CAS """
    if request.user.is_authenticated():
        return get_connection_successful(request.user.get_username())
    payutcli = payutc.Client()
    content = json.loads(request.body)
    for i in ('ticket', 'service'):
        if i not in content.keys():
            content[i] = None
    serial = core_serializers.LoginInputSerializer(data={'ticket': content['ticket'],
                                                         'service': content['service']})
    serial.is_valid(raise_exception=True)
    data = serial.validated_data
    login_given = payutcli.loginCas(ticket=data['ticket'], service=data['service'])[0]
    if 'Invalid credentials' in login_given:
        raise ValidationError('CAS login failed')
    user = authenticate(username=login_given)
    if user is None:
        if core_models.UserRight.objects.filter\
        (login=login_given).exclude(right=core_models.UserRight.USERRIGHT_NONE).count():
            user = user_creation(login_given)
        else:
            raise PermissionDenied('User has no right')
    user.is_staff = core_models.UserRight.objects.filter\
    (login=login_given, right=core_models.UserRight.USERRIGHT_ARTICLES).count() > 0
    user.is_superuser = core_models.UserRight.objects.filter\
    (login=login_given, right=core_models.UserRight.USERRIGHT_ALL).count() > 0
    user.save()
    if user.is_active:
        user = authenticate(username=login_given)
        login(request, user)
    else:
        raise PermissionDenied('Account deactivated')
    t = Token.objects.get_or_create(user=user)[0]
    return get_connection_successful(login_given, t)

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def get_my_rights(request):
    """ Obtenir ses droits utilisateurs """
    if not request.user.is_authenticated():
        return Response('NOT CONNECTED')
    login_given = request.user.username
    if core_models.UserRight.objects.filter\
    (login=login_given, right=core_models.UserRight.USERRIGHT_ALL).count() > 0:
        return Response('ALL')
    elif core_models.UserRight.objects.filter\
    (login=login_given, right=core_models.UserRight.USERRIGHT_ARTICLES).count() > 0:
        return Response('ARTICLES')
    else:
        return Response('NONE')

@api_view(['GET'])
@permission_classes((IsAuthorizedUser, ))
@renderer_classes((JSONRenderer, ))
def logout(request):
    """ Se déconnecter """
    Token.objects.filter(user=request.user).delete()
    return Response(True)

@api_view(['GET'])
@permission_classes((IsAdmin, ))
@renderer_classes((JSONRenderer, ))
def get_user_list(request):
    """
    Obtenir la liste des utilisateurs et administrateurs
    avec leur nom
    """
    names = {user_right.login: {'right': user_right.right} for user_right in core_models.UserRight.objects.all()}
    users = User.objects.filter(username__in=names.keys())
    for user in users:
        names[user.username]['name'] = ' '.join([user.first_name, user.last_name])
    return Response([{'login': login, 'name': names[login]['name'], 'right': names[login]['right']} for login in names])
