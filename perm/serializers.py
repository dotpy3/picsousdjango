from rest_framework import serializers

from facture import serializers as facture_serializers
from perm import models as perm_models


class PermSerializer(serializers.ModelSerializer):
    class Meta:
        model = perm_models.Perm


class ArticleSerializer(serializers.ModelSerializer):
    ventes = serializers.IntegerField(read_only=True)
    ventes_last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = perm_models.Article
        fields = ('stock', 'nom', 'prix', 'perm', 'ventes', 'tva',
                  'ventes_last_update', 'id_payutc')

ArticleListSerializer = ArticleSerializer.many_init


class PermWithArticleSerializer(serializers.ModelSerializer):
    article_set = ArticleListSerializer()
    facturerecue_set = facture_serializers.FactureRecueListSerializer()

    class Meta:
        model = perm_models.Perm
