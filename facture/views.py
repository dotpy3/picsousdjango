from sets import Set

from django.shortcuts import render
from rest_framework import viewsets

from core import viewsets as core_viewsets
from facture import models as facture_models
from facture import serializers as facture_serializers


class FactureRecueViewSet(viewsets.ModelViewSet):

    queryset = facture_models.FactureRecue.objects.all()
    serializer_class = facture_serializers.FactureRecueSerializer


class CategorieFactureRecueViewSet(viewsets.ModelViewSet):

    queryset = facture_models.CategorieFactureRecue.objects.all()
    serializer_class = facture_serializers.FactureRecueSerializer


class FactureEmiseViewSet(core_viewsets.RetrieveSingleInstanceModelViewSet):

    queryset = facture_models.FactureEmise.objects.all()
    single_serializer_class = facture_serializers.FactureEmiseWithRowsSerializer
    serializer_class = facture_serializers.FactureEmiseSerializer


class FactureEmiseRowViewSet(viewsets.ModelViewSet):

    queryset = facture_models.FactureEmiseRow.objects.all()
    serializer_class = facture_serializers.FactureEmiseRowSerializer


class ChequeViewSet(viewsets.ModelViewSet):

    queryset = facture_models.Cheque.objects.all()
    serializer_class = facture_serializers.ChequeSerializer


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
