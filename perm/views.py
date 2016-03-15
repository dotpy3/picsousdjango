from sets import Set

from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import get_template

from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core import viewsets as core_viewsets
from perm import models as perm_models
from perm import serializers as perm_serializers
from picsous.settings import DEFAULT_FROM_EMAIL


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
    info = perm.get_convention_information()
    print(repr(info['articles']))
    return render(request, 'convention_partenariat.html',
                  {'perm': perm, 'articles': info['articles'],
                   'montant': round(perm.get_montant_deco_max(), 2),
                   'mail': False})


def justificatif_paiement(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    articles = perm.article_set.all()
    perm_articles = list()
    tva = Set()
    for article in articles:
        article_info = {'nom': article.nom, 'prix': article.prix,
                        'ventes': article.ventes, 'tva': article.tva}
        tva.add(article.tva)
        article_info['total'] = article_info['prix'] * article_info['ventes']
        perm_articles.append(article_info)
    tva_amounts = list()
    total_ht = round(sum([article.get_price_without_taxes()*article.ventes
                          for article in articles]), 2)
    for tva_type in tva:
        tva_amounts.append({'tva': tva_type,
                            'amount': round(sum([article.get_total_taxes() *
                                                 article.ventes for article
                                                 in articles
                                                 if article.tva == tva_type]),
                                            2)})
    total_ttc = round(sum([article.prix*article.ventes
                           for article in articles]), 2)
    return render(request, 'justificatif_paiement.html',
                  {'perm': perm, 'articles': perm_articles,
                   'total_ht': total_ht, 'total_ttc': total_ttc,
                   'tva_amounts': tva_amounts})


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

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def get_article_sales(request, id):
    a = perm_models.Article.objects.get(pk=id)
    return Response(a.update_ventes())

@api_view(['GET'])
@renderer_classes((JSONRenderer, ))
def create_payutc_article(request, id):
    article = perm_models.Article.objects.get(pk=id)
    article.create_payutc_article()
    return Response(True)


@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def send_convention(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    convention_template = get_template('convention_partenariat.html')
    convention_context = {
      'perm': perm,
      'articles': perm.get_convention_information()['articles'],
      'montant': round(perm.get_montant_deco_max(), 2),
      'mail': True,
    }
    context_content = convention_template.render(convention_context)
    send_mail('Convention Perm Pic\'Asso', 'Pour lire ce message, merci d\'utiliser un navigateur ou un client mail compatible HTML.',
      DEFAULT_FROM_EMAIL, [perm.mail_resp], html_message=context_content)
    return Response(True)
