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
