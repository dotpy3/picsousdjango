# coding: utf-8

"""
Ensemble des permissions d'accès
"""

from rest_framework.permissions import BasePermission

from core.models import UserRight


class IsAuthorizedUser(BasePermission):
    """
    Vérifie que l'utilisateur est autorisé à utiliser Picsous
    => Droit réservé à l'équipe du Pic et aux éventuels consultants
    """
    def has_permission(self, request, view):
        return request.user and (UserRight.objects.filter(login=request.user.username, right__in=(UserRight.USERRIGHT_ALL, UserRight.USERRIGHT_ARTICLES)).count())


class IsAdmin(BasePermission):
    """
    Vérifie que l'utilisateur est administrateur de Picsous
    => Droit réservé au bureau, à la trésorerie, à l'équipe Info
    """
    def has_permission(self, request, view):
        return request.user and (UserRight.objects.filter(login=request.user.username, right=UserRight.USERRIGHT_ALL).count())
