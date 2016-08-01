# -*- coding: utf-8 -*-

from rest_framework import routers
from core import views as core_views
from facture import views as facture_views
from perm import views as perm_views

""" Le routeur est une fonctionnalité de Django REST Framework qui permet de récupérer
un viewset REST, et de le convertir en route.
On l'enregistre en mettant l'adresse de la route (avec une regex, de la même façon qu'en
Django), et le viewset.


	Explications Viewset :

==> si tu ne sais pas ce qu'est une API REST, renseigne-toi avant de lire la suite

Un Viewset est un objet qui représente un endpoint REST. Le viewset le plus utilisé, ModelViewSet,
est un viewset qui donne accès à toute la gamme d'actions REST possibles (GET, POST, PUT, OPTIONS,
etc...)
Il est possible de modifier l'effet des actions REST en surchargant les méthodes associées dans le viewset.
Par exemple, dans core/viewsets.py, on a rajouté un viewset qui permet de changer le serializer de sortie
lorsqu'il n'y a qu'une seule instance qui est récupéré (par un GET en /{type}/{id}/, par exemple).

Lorsqu'on crée un viewset pour un modèle, il faut lui attribuer deux paramètres :
	- queryset : La requête pour récupérer les objets (de type [Modèle].objects.all())
	- serializer_class : Le serializer qu'on utilisera pour traiter en entrée et en sortie les objets.


On a donc ajouté dans le routeur tous les viewsets de tous les objets modifiables à travers des
endpoints REST.

"""

router = routers.DefaultRouter()

# Core
router.register(r'bug', core_views.BugReportViewset)
router.register(r'periodetva', core_views.PeriodeTVAViewset)
router.register(r'userright', core_views.UserRightViewset)

# Perms
router.register(r'perms', perm_views.PermViewSet)
router.register(r'permnames', perm_views.SimplePermViewSet)
router.register(r'articles', perm_views.ArticleViewSet)
router.register(r'articlesAdmin', perm_views.ArticleAdminViewSet)

# Factures
router.register(r'facturesRecues', facture_views.FactureRecueViewSet)
router.register(r'categoriesFactureRecue', facture_views.CategorieFactureRecueViewSet)
router.register(r'factureEmises', facture_views.FactureEmiseViewSet)
router.register(r'factureEmiseRows', facture_views.FactureEmiseRowViewSet)
router.register(r'cheques', facture_views.ChequeViewSet)
