from rest_framework import serializers

from facture import serializers as facture_serializers
from perm import models as perm_models


class PermSerializer(serializers.ModelSerializer):
    facturerecue_set = facture_serializers.SimpleFactureRecueListSerializer(read_only=True, required=False)
    class Meta:
        model = perm_models.Perm


class SimplePermSerializer(serializers.ModelSerializer):
    class Meta:
        model = perm_models.Perm
        fields = ('id', 'nom', 'date')


class ArticleSerializer(serializers.ModelSerializer):
    ventes = serializers.IntegerField(read_only=True)
    ventes_last_update = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = perm_models.Article
        fields = ('stock', 'nom', 'prix', 'perm', 'ventes', 'tva',
                  'ventes_last_update', 'id_payutc', 'id')

ArticleListSerializer = ArticleSerializer.many_init


class PermWithArticleSerializer(serializers.ModelSerializer):
    article_set = ArticleListSerializer(read_only=True, required=False)
    facturerecue_set = facture_serializers.FactureRecueListSerializer(read_only=True, required=False)

    class Meta:
        model = perm_models.Perm
