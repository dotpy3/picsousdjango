from django.shortcuts import render
from core import viewsets as core_viewsets
from perm import models as perm_models
from perm import serializers as perm_serializers
from rest_framework import viewsets
from rest_framework.response import Response
from sets import Set


class PermViewSet(core_viewsets.RetrieveSingleInstanceModelViewSet):
    """
    Perm endpoint
    """
    queryset = perm_models.Perm.objects.all()
    serializer_class = perm_serializers.PermSerializer
    single_serializer_class = perm_serializers.PermWithArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article endpoint
    """
    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer


def convention_partenariat(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    articles = perm.article_set.all()
    perm_articles = list()
    for article in articles:
        perm_articles.append({'nom': article.nom, 'stock': article.stock, 'prixTTC': article.prix,
                              'prixHT': article.get_price_without_taxes(), 'TVA': article.tva})
    return render(request, 'convention_partenariat.html', {'perm': perm, 'articles': perm_articles,
                                                           'montant': round(perm.get_montant_deco_max(), 2)})


def justificatif_paiement(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    articles = perm.article_set.all()
    perm_articles = list()
    tva = Set()
    for article in articles:
        article_info = {'nom': article.nom, 'prix': article.prix, 'ventes': article.ventes, 'tva': article.tva}
        tva.add(article.tva)
        article_info['total'] = article_info['prix'] * article_info['ventes']
        perm_articles.append(article_info)
    tva_amounts = list()
    total_ht = round(sum([article.get_price_without_taxes()*article.ventes for article in articles]), 2)
    for tva_type in tva:
        tva_amounts.append({'tva': tva_type,
                            'amount': round(sum([article.get_total_taxes()*article.ventes
                                                 for article in articles if article.tva == tva_type]), 2)})
    total_ttc = round(sum([article.prix*article.ventes for article in articles]), 2)
    return render(request, 'justificatif_paiement.html', {'perm': perm, 'articles': perm_articles, 'total_ht': total_ht,
                                                          'total_ttc': total_ttc, 'tva_amounts': tva_amounts})


class UpdateArticleViewSet(viewsets.GenericViewSet):

    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer

    def update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        a = perm_models.Article.objects.get(pk=id)
        a.update_ventes()
        a.get_fresh()
        serializer = self.get_serializer(a)
        return Response(serializer.data)
