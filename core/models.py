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


class Semestre(models.Model):
    # Modèle représentant un semestre de cours.
    SEMESTRE_AUTOMNE = 'A'
    SEMESTRE_PRINTEMPS = 'P'

    SEMESTRE_CHOICES = (
        (SEMESTRE_AUTOMNE, 'Automne'),
        (SEMESTRE_PRINTEMPS, 'Printemps'),
    )

    annee = models.IntegerField()
    periode = models.CharField(max_length=1, choices=SEMESTRE_CHOICES)

    solde_debut = models.IntegerField(default=0)

    @classmethod
    def filter_queryset(cls, qs, request=None):
        from picsous.permissions import IsAdmin
        from constance import config as live_config
        if request:
            semester_wanted = request.GET.get("semester", False)
        if request and IsAdmin().has_permission(request, None) and semester_wanted != False:
            if semester_wanted == "all":
                return qs.all()
            elif int(semester_wanted) > 0:
                return qs.filter(semestre__id=int(semester_wanted))
        else:
            return qs.filter(semestre__id=live_config.SEMESTER)

    def get_paid_bills(self):
        from facture.models import FactureEmise, FactureRecue
        sum_paid_received_bills = sum(fac.prix
                                      for fac in FactureRecue.objects.filter(semestre=self,
                                                                             etat=FactureRecue.FACTURE_PAYEE))
        sum_paid_outvoiced_bills = sum(fac.get_total_ttc_price()
                                       for fac in FactureEmise.objects.filter(semestre=self,
                                                                              etat=FactureEmise.FACTURE_PAYEE))
        return {
            'sum_paid_received_bills': sum_paid_received_bills,
            'sum_paid_outvoiced_bills': sum_paid_outvoiced_bills,
        }


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
