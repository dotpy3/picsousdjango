from rest_framework import serializers

from facture import models as facture_models
from perm import models as perm_models


class SimplePermSerializer(serializers.ModelSerializer):
    class Meta:
        model = perm_models.Perm
        fields = ('id', 'nom')


class FactureRecueSerializer(serializers.ModelSerializer):
    personne_a_rembourser = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = facture_models.FactureRecue


FactureRecueListSerializer = FactureRecueSerializer.many_init


class CategorieFactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.CategorieFactureRecue


class FactureEmiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmise


class FactureEmiseRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmiseRow


FactureEmiseRowListSerializer = FactureEmiseRowSerializer.many_init


class ChequeSerializer(serializers.ModelSerializer):
    facturerecue = serializers.IntegerField(required=False)
    class Meta:
        model = facture_models.Cheque


class FactureEmiseWithRowsSerializer(serializers.ModelSerializer):
    factureemiserow_set = FactureEmiseRowListSerializer()

    class Meta:
        model = facture_models.FactureEmise


class TvaInfo(serializers.Serializer):
    pass
