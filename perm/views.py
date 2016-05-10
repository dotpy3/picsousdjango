# -*- coding: utf-8 -*-

from sets import Set

from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import get_template

from dal import autocomplete

from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core import viewsets as core_viewsets
from facture import models as facture_models
from perm import models as perm_models
from perm import serializers as perm_serializers
from picsous.settings import DEFAULT_FROM_EMAIL

"""
Note globale pour ce fichier :

Dans ce fichier, en dehors des viewsets (expliqués dans picsous/routeur.py), les vues
simples sont déclarées de deux façons :
- de façon générique Django, avec une fonction qui va se terminer par le retour d'un
render d'une template Django.
- de façon Django REST Framework - cette façon permet de définir clairement les méthodes
HTTP par lesquelles une vue peut être atteinte, et permet de prédéfinir le Content-Type
dans lequel la réponse sera rendue.
Par exemple, pour les vues qui sont sensées retourner du JSON, on utilisera le
renderer REST Framework appelé JSONRenderer.

Ces deux vues peuvent être distinguées par l'utilisation des décorateurs api_view (définition
des méthodes HTTP) et renderer_class (content type du retour), qui sont caractéristiques de
la vue REST Framework.

L'intérêt d'une vue générique Django est de permettre de render une vue, tandis que celle
de la vue Django REST Framework est de pouvoir retourner facilement dans un format voulu.
On utilisera donc principalement les vues traditionnelles pour afficher des pages, et des
vues REST Framework pour des appels d'API (qui serviront, par exemple, en appel AJAX).

"""


class PermViewSet(core_viewsets.RetrieveSingleInstanceModelViewSet):
    """
    Perm viewset
    """
    queryset = perm_models.Perm.objects.all()
    serializer_class = perm_serializers.PermSerializer
    single_serializer_class = perm_serializers.PermWithArticleSerializer
    permission_classes = (IsAuthenticated,)


class SimplePermViewSet(mixins.ListModelMixin, viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin):
    """
    Perm simple viewset: pour récupérer la liste des perms avec juste le nom et l'id
    """
    queryset = perm_models.Perm.objects.all()
    serializer_class = perm_serializers.SimplePermSerializer
    permission_classes = (IsAuthenticated,)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article viewset
    """
    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer
    permission_classes = (IsAuthenticated,)


def convention_partenariat(request, id):
    """
    Vue qui permet d'afficher la convention de partenariat de perm d'id {id}.
    On récupère les informations en méthode de l'objet, et on va ensuite juste
    traiter la template et la render.
    """
    perm = perm_models.Perm.objects.get(pk=id)
    info = perm.get_convention_information()
    return render(request, 'convention_partenariat.html',
                  {'perm': perm, 'articles': info['perm_articles'],
                   'montant': round(perm.get_montant_deco_max(), 2),
                   'mail': False})


def justificatif_paiement(request, id):
    """
    Vue qui permet d'afficher le justificatif de paiement de perm d'id {id}, de la
    même façon que la convention de partenariat.
    ATTENTION : l'appel de cette vue ne met pas à jour les ventes. Il est donc
    indispensable, à travers le viewset UpdateArticleViewSet, de mettre à jour les
    ventes pour cet article. Sinon quoi, le justificatif de paiement sera invalide.
    """
    perm = perm_models.Perm.objects.get(pk=id)
    info = perm.get_justificatif_information()
    return render(request, 'justificatif_paiement.html',
                  {'perm': perm, 'articles': info['perm_articles'],
                   'total_ht': info['total_ht'], 'total_ttc': info['total_ttc'],
                   'tva_amounts': info['tva_amounts'], 'mail': False})


class UpdateArticleViewSet(viewsets.GenericViewSet):
    """
    Viewset qui génère un endpoint qui, lorsqu'appelé en PUT, récupère auprès de
    PayUTC les ventes de l'article {id} (id étant passé en paramètre dans l'URL).
    """

    queryset = perm_models.Article.objects.all()
    serializer_class = perm_serializers.ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        a = perm_models.Article.objects.get(pk=id)
        a.update_ventes()
        a.get_fresh()
        serializer = self.get_serializer(a)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def get_article_sales(request, id):
    # Endpoint qui permet d'obtenir, pour un article de pk {id}, d'obtenir les ventes de l'article.
    a = perm_models.Article.objects.get(pk=id)
    return Response(a.update_ventes())

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def create_payutc_article(request, id):
    # Endpoint qui permet d'obtenir, pour un article de pk {id}, d'enregistrer l'article dans PayUTC.
    article = perm_models.Article.objects.get(pk=id)
    article.create_payutc_article()
    return Response(True)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def get_perm_sales(request, id):
    p = perm_models.Perm.objects.get(pk=id)
    return Response(p.get_justificatif_information())

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def delete_facture_recue(request, id):
    fr = facture_models.FactureRecue.objects.get(pk=id)
    fr.delete()
    return Response(True)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def send_convention(request, id):
    """
    Endpoint qui permet d'envoyer la convention de partenariat par mail pour une perm
    d'id {id}.
    """
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


class PermNameAutocomplete(autocomplete.Select2QuerySetView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.q:
            return perm_models.Perm.objects.none()
        qs = perm_models.Perm.objects.filter(nom__icontains=self.q)

        return qs


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@renderer_classes((JSONRenderer, ))
def send_justificatif(request, id):
    """
    Endpoint qui permet d'envoyer le justificatif de paiement par mail pour une perm
    d'id {id}.
    """
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
