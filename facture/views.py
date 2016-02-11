from rest_framework import viewsets

from facture import models as facture_models
from facture import serializers as facture_serializers


class FactureRecueViewSet(viewsets.ModelViewSet):

    queryset = facture_models.FactureRecue.objects.all()
    serializer_class = facture_serializers.FactureRecueSerializer


class CategorieFactureRecueViewSet(viewsets.ModelViewSet):

    queryset = facture_models.CategorieFactureRecue.objects.all()
    serializer_class = facture_serializers.FactureRecueSerializer
