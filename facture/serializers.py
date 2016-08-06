from rest_framework import serializers

from facture import models as facture_models
from perm import models as perm_models


class SimplePermSerializer(serializers.ModelSerializer):
    class Meta:
        model = perm_models.Perm
        fields = ('id', 'nom')


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.Cheque


ChequeListSerializer = ChequeSerializer.many_init


class SimpleFactureRecueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = facture_models.FactureRecue
        fields = ('id', )

SimpleFactureRecueListSerializer = SimpleFactureRecueSerializer.many_init


class FactureRecueSerializer(serializers.ModelSerializer):
    cheque_set = ChequeListSerializer(required=False)
    personne_a_rembourser = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    date_paiement = serializers.DateField(required=False, allow_null=True)
    date_remboursement = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = facture_models.FactureRecue
        exclude = ('semestre', )


FactureRecueListSerializer = FactureRecueSerializer.many_init


class CategorieFactureRecueSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.CategorieFactureRecue


class FactureEmiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmise
        exclude = ('semestre', )


class FactureEmiseRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture_models.FactureEmiseRow


FactureEmiseRowListSerializer = FactureEmiseRowSerializer.many_init


class FactureEmiseWithRowsSerializer(serializers.ModelSerializer):
    factureemiserow_set = FactureEmiseRowListSerializer()

    class Meta:
        model = facture_models.FactureEmise
        exclude = ('semestre',)


class TvaInfo(serializers.Serializer):
    pass
