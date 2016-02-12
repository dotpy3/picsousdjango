from rest_framework import serializers

from facture import models as facture_models


class FactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureRecue


class CategorieFactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.CategorieFactureRecue


class FactureEmiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmise


class FactureEmiseRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmiseRow


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.Cheque


class FactureEmiseWithRowsSerializer(serializers.ModelSerializer):
    factureemiserow_set = FactureEmiseRowSerializer()

    class Meta:
        model = facture_models.FactureEmise


class TvaInfo(serializers.Serializer):
    pass
