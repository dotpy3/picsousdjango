# coding: utf8
""" Modeles de base de picsous """

from __future__ import unicode_literals

from django.db import models

class UserRight(models.Model):
    """
    Modèle de gestion des droits utilisateurs.
    On distingue plusieurs types de droits, à travers la valeur de 'right'.
    Par défaut, un utilisateur qui n'a aucun UserRight revient à un utilisateur
    qui a un utilisateur qui a comme right 'USERRIGHT_NONE'

    XXX : distinguer quelqu'un qui a tous les droits sur la tréso (type, l'équipe tréso)
    de ceux qui tous les droits (type, l'équipe info).
    """
    USERRIGHT_ALL = 'A'
    USERRIGHT_ARTICLES = 'P'
    USERRIGHT_NONE = 'N'

    USERRIGHT_CHOICES = (
        (USERRIGHT_ALL, 'Accès total'),
        (USERRIGHT_ARTICLES, 'Accès articles'),
        (USERRIGHT_NONE, 'Accès interdit'),
    )

    login = models.CharField(max_length=10, unique=True)
    right = models.CharField(max_length=1, choices=USERRIGHT_CHOICES)


class BugReport(models.Model):
    """
    Rapport de bug : les identifiants reporter sont relatifs au profil de celui qui
    dépose le rapport de bug.
    """
    STATE_NOT_RESOLVED = 'N'
    STATE_IN_PROGRESS = 'P'
    STATE_RESOLVED = 'R'

    STATE_CHOICES = (
        (STATE_NOT_RESOLVED, 'Non résolu'),
        (STATE_IN_PROGRESS, 'En cours'),
        (STATE_RESOLVED, 'Terminé'),
    )

    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    reporter_name = models.CharField(max_length=255)
    reporter_mail = models.CharField(max_length=255)
    content = models.TextField()


class TimeModel(models.Model):
    """ Modèle représentant une période temporelle """
    class Meta(object):
        """ Représentation en DB """
        abstract = True

    debut = models.DateField()
    fin = models.DateField()


class PeriodeTVA(TimeModel):
    """
    Période de TVA.
    """
    PERIODE_NON_DECLAREE = 'N'
    PERIODE_DECLAREE = 'D'

    PERIODE_CHOICES = (
        (PERIODE_NON_DECLAREE, 'Non déclarée'),
        (PERIODE_DECLAREE, 'Déclarée'),
    )

    state = models.CharField(max_length=1, choices=PERIODE_CHOICES, default='N')

    class Meta:
        """ Représentation en DB """
        abstract = False


class PricedModel(models.Model):
    """
    Classe abstraite qui représente tout objet qui a un prix.
    """
    tva = models.FloatField(default=0) # TVA en decimal, type 5.5, 20...
    prix = models.FloatField(default=0) # prix TTC

    def get_price_without_taxes(self):
        """ À partir du prix TTC sauvegardé de l'objet, obtenir le prix HT """
        return round(self.prix * (100 / (100 + self.tva)), 2)

    def get_total_taxes(self):
        """ À partir du prix TTC sauvegardé de l'objet, obtenir la TVA """
        return round(self.prix - self.get_price_without_taxes(), 2)

    class Meta:
        """ Représentation en DB """
        abstract = True
