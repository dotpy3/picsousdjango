from rest_framework import serializers

from facture import models as facture_models


class FactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureRecue


class CategorieFactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.CategorieFactureRecue
