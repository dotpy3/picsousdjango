# coding: utf8

from django.db import models

from core import models as core_models
from perm import models as perm_models


class CategorieFactureRecue(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=1)


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
    commentaire = models.TextField(null=True, default=None)
    cheque = models.ForeignKey(FactureRecue, null=True)


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
    date_creation = models.DateField(auto_now_add=True)
    nom_createur = models.CharField(max_length=255)
    date_paiement = models.DateField(null=True)
    date_due = models.DateField()
    etat = models.CharField(max_length=1, choices=FACTURE_STATES)

    def get_total_ht_price(self):
        rows = self.factureemiserow_set.all()
        return round(sum([row.get_total_ht_price() for row in rows]), 2)

    def get_total_ttc_price(self):
        rows = self.factureemiserow_set.all()
        return round(sum([row.get_total_ttc_price() for row in rows]), 2)


class FactureEmiseRow(core_models.PricedModel):
    facture = models.ForeignKey(FactureEmise)
    nom = models.CharField(max_length=255)
    qty = models.IntegerField()

    def get_total_ttc_price(self):
        return self.prix * self.qty

    def get_total_ht_price(self):
        return self.qty * self.get_price_without_taxes()

    def get_total_taxes_for_row(self):
        return self.qty * self.get_total_taxes()
