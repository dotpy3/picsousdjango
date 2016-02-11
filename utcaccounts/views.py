#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

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
