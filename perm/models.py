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

    nom = models.CharField(max_length=255)
    asso = models.BooleanField(default=True)  # true if asso
    nom_resp = models.CharField(null=True, default=None, max_length=255)
    mail_resp = models.CharField(null=True, default=None, max_length=255)
    tel_resp = models.CharField(null=True, default=None, max_length=255)
    role = models.CharField(null=True, default=None, max_length=255)
    date = models.DateField()
    periode = models.CharField(choices=PERIOD_VALUES, max_length=1)
    montantTTCMaxAutorise = models.FloatField(null=True, default=None)
    remarque = models.TextField(null=True, default=None)

    def get_montant_deco_max(self):
        if self.montantTTCMaxAutorise:
            return self.montantTTCMaxAutorise
        if self.date.weekday() in [3, 4]:
            return 30
        else:
            return 20


class Article(core_models.PricedModel):
    id_payutc = models.IntegerField(null=True, default=None)
    stock = models.IntegerField(default=0)
    ventes = models.IntegerField(default=0)
    ventes_last_update = models.DateTimeField(null=True, default=None)
    nom = models.CharField(max_length=255)
    perm = models.ForeignKey(Perm)

    def create_payutc_article(self):
        c = payutc.Client()
        c.loginApp()
        c.loginBadge()
        rep = c.call('GESARTICLES', 'setArticle', active=True, alcool=False,
                     components=[], cotisant=True,
                     fun_id=NEMOPAY_FUNDATION_ID, image_path='', meta=dict(),
                     name=self.nom, pack=False,
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
            return False
        self.ventes = sales[0]
        self.ventes_last_update = timezone.now()
        self.save()
        return self.ventes
