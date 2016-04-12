# -*- coding: utf-8 -*-

from sets import Set

from django.db import models
from django.utils import timezone

from core import models as core_models
from core.services import payutc
from picsous.settings import NEMOPAY_FUNDATION_ID, NEMOPAY_ARTICLES_CATEGORY


class Perm(models.Model):
    PERIOD_MATIN = 'M'
    PERIOD_MIDI = 'D'
    PERIOD_SOIR = 'S'

    PERIOD_VALUES = (
        (PERIOD_MATIN, 'Matin'),
        (PERIOD_MIDI, 'Midi'),
        (PERIOD_SOIR, 'Soir'),
    )

    PERM_TRAITEE = 'T'
    PERM_NON_TRAITEE = 'N'

    PERM_STATE_VALUES = (
        (PERM_TRAITEE, 'Traitée'),
        (PERM_NON_TRAITEE, 'Non traitée'),
    )

    nom = models.CharField(max_length=255)
    asso = models.BooleanField(default=True)  # true if asso
    nom_resp = models.CharField(null=True, default=None, max_length=255)
    mail_resp = models.CharField(null=True, default=None, max_length=255)
    tel_resp = models.CharField(null=True, default=None, max_length=255)
    role = models.CharField(null=True, default=None, max_length=255)
    date = models.DateField()
    periode = models.CharField(choices=PERIOD_VALUES, max_length=1)
    state = models.CharField(choices=PERM_STATE_VALUES, max_length=1, default='N')
    montantTTCMaxAutorise = models.FloatField(null=True, default=None)
    remarque = models.TextField(null=True, default=None)

    def __str__(self):
        return self.nom
    
    def get_montant_deco_max(self):
        if self.montantTTCMaxAutorise:
            return self.montantTTCMaxAutorise
        if self.date.weekday() in [3, 4]:
            return 30
        else:
            return 20

    def get_convention_information(self):
        articles = self.article_set.all()
        perm_articles = list()
        for article in articles:
            perm_articles.append({'nom': article.nom, 'stock': article.stock,
                                  'prixTTC': article.prix,
                                  'prixHT': article.get_price_without_taxes(),
                                  'TVA': article.tva})
        return {
            'perm': self,
            'articles': articles,
            'perm_articles': perm_articles,
        }

    def get_justificatif_information(self):
        articles = self.article_set.all()
        perm_articles = list()
        tva = Set()
        for article in articles:
            article_info = {'nom': article.nom, 'prix': article.prix,
                            'ventes': article.ventes, 'tva': article.tva}
            tva.add(article.tva)
            article_info['total'] = article_info['prix'] * article_info['ventes']
            perm_articles.append(article_info)
        tva_amounts = list()
        total_ht = round(sum([article.get_price_without_taxes()*article.ventes
                              for article in articles]), 2)
        for tva_type in tva:
            tva_amounts.append({'tva': tva_type,
                                'amount': round(sum([article.get_total_taxes() *
                                                     article.ventes for article
                                                     in articles
                                                     if article.tva == tva_type]),
                                                2)})
        total_ttc = round(sum([article.prix*article.ventes
                               for article in articles]), 2)
        return {
            'perm_articles': perm_articles,
            'total_ht': total_ht,
            'total_ttc': total_ttc,
            'tva_amounts': tva_amounts,
        }


class Article(core_models.PricedModel):
    id_payutc = models.IntegerField(null=True, default=None)
    stock = models.IntegerField(default=0)
    ventes = models.IntegerField(default=0)
    ventes_last_update = models.DateTimeField(null=True, default=None)
    nom = models.CharField(max_length=255)
    perm = models.ForeignKey(Perm)

    def create_payutc_article(self):
        if self.id_payutc:
            return self.id_payutc
        c = payutc.Client()
        c.loginApp()
        c.loginBadge()
        rep = c.call('GESARTICLE', 'setProduct', active=True, alcool=False, cotisant=True,
                     components=[],
                     fun_id=NEMOPAY_FUNDATION_ID, image_path='', meta=dict(),
                     name=self.nom + ' - ' + self.perm.nom, pack=False,
                     parent=NEMOPAY_ARTICLES_CATEGORY, prices=[],
                     prix=int(self.prix*100), stock=self.stock,
                     tva=self.tva, variable_price=False, virtual=False)
        self.id_payutc = int(rep['success'])
        self.ventes_last_update = timezone.now()
        self.save()
        return self.id_payutc

    def update_ventes(self):
        c = payutc.Client()
        c.loginApp()
        c.loginBadge()
        rep = c.call('TRESO', 'getExport', fun_id=NEMOPAY_FUNDATION_ID)
        sales = [obj['quantity'] for obj in rep
                 if obj['obj_id'] == self.id_payutc]
        if len(sales) == 0:
            self.ventes = 0
        else:
            self.ventes = sales[0]
        self.ventes_last_update = timezone.now()
        self.save()
        return self.ventes
