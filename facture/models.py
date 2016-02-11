# coding: utf8

from django.db import models

from core import models as core_models
from perm import models as perm_models


class CategorieFactureRecue(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=1)


class Cheque(models.Model):
    CHEQUE_ENCAISSE = 'E'
    CHEQUE_ANNULE = 'A'
    CHEQUE_CAUTION = 'C'

    CHEQUE_STATES = (
        (CHEQUE_ENCAISSE, 'Encaisse'),
        (CHEQUE_ANNULE, 'Annulé'),
        (CHEQUE_CAUTION, 'Caution'),
    )

    num = models.IntegerField()
    valeur = models.FloatField(default=0)
    state = models.CharField(max_length=1, choices=CHEQUE_STATES)
    destinataire = models.CharField(max_length=255, null=True, default=None)


class FactureRecue(core_models.PricedModel):
    perm = models.ForeignKey(perm_models.Perm, null=True, default=None)
    categorie = models.ForeignKey(CategorieFactureRecue, null=True)
    nom_entreprise = models.CharField(max_length=255)
    date = models.DateField()
    date_paiement = models.DateField(null=True, default=None)
    date_remboursement = models.DateField(null=True, default=None)
    moyen_paiement = models.CharField(null=True, default=None, max_length=255)
    personne_a_rembourser = models.CharField(null=True, default=None, max_length=255)
    immobilisation = models.BooleanField(default=False)
    remarque = models.TextField(null=True, default=None)
    cheque = models.ForeignKey(Cheque, null=True)


class FactureEmise(models.Model):

    FACTURE_DUE = 'D'
    FACTURE_ANNULEE = 'A'
    FACTURE_PARTIELLEMENT_PAYEE = 'T'
    FACTURE_PAYEE = 'P'

    FACTURE_STATES = (
        (FACTURE_DUE, 'Due'),
        (FACTURE_ANNULEE, 'Annulée'),
        (FACTURE_PARTIELLEMENT_PAYEE, 'Partiellement payée'),
        (FACTURE_PAYEE, 'Payée'),
    )

    destinataire = models.CharField(max_length=255)
    date_creation = models.DateField()
    nom_createur = models.CharField(max_length=255)
    date_paiement = models.DateField()
    date_due = models.DateField()
    etat = models.CharField(max_length=1, choices=FACTURE_STATES)


class FactureEmiseRow(core_models.PricedModel):
    nom = models.CharField(max_length=255)
    qty = models.IntegerField()
