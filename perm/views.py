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
    return render(request, 'convention_partenariat.html',
                  {'perm': perm, 'articles': info['perm_articles'],
                   'montant': round(perm.get_montant_deco_max(), 2),
                   'mail': False})


def justificatif_paiement(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    info = perm.get_justificatif_information()
    return render(request, 'justificatif_paiement.html',
                  {'perm': perm, 'articles': info['perm_articles'],
                   'total_ht': info['total_ht'], 'total_ttc': info['total_ttc'],
                   'tva_amounts': info['tva_amounts'], 'mail': False})


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
      'articles': perm.get_convention_information()['perm_articles'],
      'montant': round(perm.get_montant_deco_max(), 2),
      'mail': True,
    }
    context_content = convention_template.render(convention_context)
    send_mail('Convention Perm Pic\'Asso', 'Pour lire ce message, merci d\'utiliser un navigateur ou un client mail compatible HTML.',
      DEFAULT_FROM_EMAIL, [perm.mail_resp], html_message=context_content)
    return Response(True)


@api_view(['POST'])
@renderer_classes((JSONRenderer, ))
def send_justificatif(request, id):
    perm = perm_models.Perm.objects.get(pk=id)
    info = perm.get_justificatif_information()
    justificatif_template = get_template('justificatif_paiement.html')
    justificatif_context = {
      'perm': perm, 'articles': info['perm_articles'], 'total_ht': info['total_ht'],
      'total_ttc': info['total_ttc'], 'tva_amounts': info['tva_amounts'], 'mail': True,
    }
    context_content = justificatif_template.render(justificatif_context)
    send_mail('Justificatif paiement Pic\'Asso', 'Pour lire ce message, merci d\'utiliser un navigateur ou un client mail compatible HTML.',
      DEFAULT_FROM_EMAIL, [perm.mail_resp], html_message=context_content)
    return Response(True)
