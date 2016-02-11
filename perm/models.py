from django.db import models

from core.services import payutc
from picsous.settings import NEMOPAY_CONNECTION_PIN, NEMOPAY_CONNECTION_UID, NEMOPAY_FUNDATION_ID,\
    NEMOPAY_ARTICLES_CATEGORY


class Perm(models.Model):
    PERIOD_MATIN = 'M'
    PERIOD_MIDI = 'D'
    PERIOD_SOIR = 'S'

    PERIOD_VALUES = (
        (PERIOD_MATIN, 'Matin'),
        (PERIOD_MIDI, 'Midi'),
        (PERIOD_SOIR, 'Soir'),
    )

    nom = models.CharField(max_length=255)
    asso = models.BooleanField(default=True) # true if asso
    nom_resp = models.CharField(null=True, default=None, max_length=255)
    mail_resp = models.CharField(null=True, default=None, max_length=255)
    tel_resp = models.CharField(null=True, default=None, max_length=255)
    role = models.CharField(null=True, default=None, max_length=255)
    date = models.DateField()
    periode = models.CharField(choices=PERIOD_VALUES, max_length=1)
    montantTTCMaxAutorise = models.FloatField(null=True, default=None)
    montantDecoHT = models.FloatField(default=0)
    montantDecoTVA = models.FloatField(default=0)
    remarque = models.TextField(null=True, default=None)


class Article(models.Model):
    id_payutc = models.IntegerField(null=True, default=None)
    stock = models.IntegerField(default=0)
    ventes = models.IntegerField(default=0)
    tva = models.FloatField(default=0)
    prix = models.IntegerField(default=0)
    nom = models.IntegerField()
    perm = models.ForeignKey(Perm)

    def create_payutc_article(self):
        c = payutc.Client()
        c.call('POSS3', 'loginBadge', badge_uid=NEMOPAY_CONNECTION_UID, pin=NEMOPAY_CONNECTION_PIN)
        rep = c.call('GESARTICLES', 'setArticle', active=True, alcool=False, components=[], cotisant=True,
                     fun_id=NEMOPAY_FUNDATION_ID, image_path='', meta=dict(), name=self.nom, pack=False,
                     parent=NEMOPAY_ARTICLES_CATEGORY, prices=[], prix=int(self.prix*100), stock=self.stock,
                     tva=self.tva, variable_price=False, virtual=False)
        self.id_payutc = int(rep['success'])
        self.save()
        return self.id_payutc

    def update_ventes(self):
        c = payutc.Client()
        c.call('POSS3', 'loginBadge', badge_uid=NEMOPAY_CONNECTION_UID, pin=NEMOPAY_CONNECTION_PIN)
        rep = c.call('TRESO', 'getExport', fun_id=NEMOPAY_FUNDATION_ID)
        sales = [obj['quantity'] for obj in rep if obj['obj_id'] == self.id_payutc]
        if len(sales) == 0:
            return False
        self.ventes = sales[0]
        self.save()
        return self.ventes
