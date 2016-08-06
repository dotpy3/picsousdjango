 # -*- coding: utf-8 -*-

from sets import Set

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from picsous.permissions import IsAdmin, IsAuthorizedUser
from picsous.settings import NEMOPAY_FUNDATION_ID

from core import models as core_models
from core import viewsets as core_viewsets
from core.services import payutc
from facture import models as facture_models
from facture import serializers as facture_serializers


class FactureRecueViewSet(viewsets.ModelViewSet):

    serializer_class = facture_serializers.FactureRecueSerializer
    permission_classes = (IsAdmin,)
    def get_queryset(self):
        qs = facture_models.FactureRecue.objects
        return core_models.Semestre.filter_queryset(qs, self.request)


class CategorieFactureRecueViewSet(viewsets.ModelViewSet):

    queryset = facture_models.CategorieFactureRecue.objects.all()
    serializer_class = facture_serializers.CategorieFactureRecueSerializer
    permission_classes = (IsAdmin,)


class FactureEmiseViewSet(core_viewsets.RetrieveSingleInstanceModelViewSet):

    single_serializer_class = facture_serializers.FactureEmiseWithRowsSerializer
    serializer_class = facture_serializers.FactureEmiseSerializer
    permission_classes = (IsAdmin,)
    def get_queryset(self):
        qs = facture_models.FactureEmise.objects
        return core_models.Semestre.filter_queryset(qs, self.request)


class FactureEmiseRowViewSet(viewsets.ModelViewSet):

    queryset = facture_models.FactureEmiseRow.objects.all()
    serializer_class = facture_serializers.FactureEmiseRowSerializer
    permission_classes = (IsAdmin,)


class ChequeViewSet(viewsets.ModelViewSet):

    queryset = facture_models.Cheque.objects.all()
    serializer_class = facture_serializers.ChequeSerializer
    permission_classes = (IsAdmin,)


def facture(request, id):
    facture = facture_models.FactureEmise.objects.get(pk=id)
    rows = list(facture.factureemiserow_set.all())
    rows_info = list()
    tva_set = Set()
    for row in rows:
        rows_info.append({'nom': row.nom, 'prixHT': row.get_price_without_taxes(), 'qty': row.qty, 'tva': row.tva,
                          'totalHT': row.get_total_ht_price(), 'totalTTC': row.get_total_ttc_price()})
        tva_set.add(row.tva)
    tva_info = list()
    for tva in tva_set:
        tva_rows = [row for row in rows if row.tva == tva]
        tva_info.append({ 'tva': tva, 'amount': round(sum([row.get_total_taxes_for_row() for row in tva_rows]), 2) })
    return render(request, 'facture.html', {'facture': facture, 'rows': rows_info, 'tva_amounts': tva_info,
                                            'total_ht': facture.get_total_ht_price(),
                                            'total_ttc': facture.get_total_ttc_price()})


@api_view(['GET'])
@permission_classes((IsAdmin, ))
@renderer_classes((JSONRenderer, ))
def tva_info(request, id):
    periode = core_models.PeriodeTVA.objects.get(pk=id)

    # Pour la TVA déductible : on veut juste obtenir le montant total de TVA
    tva_deductible = sum([facture.get_total_taxes() for facture
        in facture_models.FactureRecue.objects.filter(date__gte=periode.debut, date__lte=periode.fin)])

    # Pour la TVA à déclarer :
    #   * On récupère toute la TVA sur PayUTC pendant cette période.
    #   * On récupère toute la TVA sur les factures émises pendant cette période.
    c = payutc.Client()
    c.loginApp()
    c.loginBadge()
    sales = c.call('TRESO', 'getExport', fun_id=NEMOPAY_FUNDATION_ID, start=periode.debut.isoformat(), end=periode.fin.isoformat())
    payutc_tva_types = Set(sale['pur_tva'] for sale in sales)

    factures_emises = facture_models.FactureEmiseRow.objects.prefetch_related('facture').filter(facture__date_creation__gte=periode.debut, facture__date_creation__lte=periode.fin)
    tva_types = payutc_tva_types.union(Set(facture.tva for facture in factures_emises))

    tva_a_declarer = list()
    for tva_type in tva_types:
        tva_a_declarer.append({'pourcentage': tva_type,
                               'montant': sum([(1 - (100 / (100 + sale['pur_tva'])))*sale['total']*0.01 for sale in sales if sale['pur_tva'] == tva_type])
                               + sum(facture.get_total_taxes() * facture.qty for facture in factures_emises if facture.tva == tva_type)})

    return Response({'tva_deductible': tva_deductible,
                     'tva_a_declarer': tva_a_declarer,
                     'tva_a_declarer_total': sum(tva['montant'] for tva in tva_a_declarer)})
