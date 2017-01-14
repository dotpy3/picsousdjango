# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from utcaccounts.urls import urlpatterns as utcaccounts_urlpatterns

from core import views as core_views
from facture import views as facture_views
from perm import views as perm_views
from utcaccounts import views as utcaccounts_views
from router import router

"""
C'est ici, dans les URLs de l'application, que toutes les routes sont déclarées.

C'est la variable urlpatterns qui les regroupe, qui est ensuite récupérée par Django
pour en tirer les URLS.

Les URLs sont déclarées :
- individuellement, pour les routes qui effectuent des actions précises (envoi de
convention, affichage de documents, génération d'article PayUTC...)
- récupérées par le routeur, pour les routes générées par Django REST Framework. C'est
le include qui est utilisé, et qui récupère auprès du routeur toutes les routes
créées.
"""

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^autocomplete/(?P<query>\w+)$', core_views.autocomplete),
    url(r'^getCurrentCredit', core_views.semester_beginning_credit),
    url(r'^getAdminSettings$', core_views.get_admin_settings),
    url(r'^getSemestreState$', core_views.semestre_state),
    url(r'^editSettings$', core_views.save_admin_settings),
    url(r'^getBadge$', core_views.get_badge),

    url(r'^facture/(?P<id>\d+)$', facture_views.facture),
    url(r'^tvainfo/(?P<id>\d+)$', facture_views.tva_info),
    url(r'^generate/cheques$', facture_views.excel_check_generation),
    url(r'^generate/factures$', facture_views.excel_facture_generation),

    url(r'^convention/(?P<id>\d+)$', perm_views.convention_partenariat),
    url(r'^createpayutcarticle/(?P<id>\d+)/$', perm_views.create_payutc_article),
    url(r'^deletefacturerecue/(?P<id>\d+)/$', perm_views.delete_facture_recue),
    url(r'^justificatif/(?P<id>\d+)$', perm_views.justificatif_paiement),
    url(r'^sendjustificatif/(?P<id>\d+)$', perm_views.send_justificatif),
    url(r'^permsales/(?P<id>\d+)/$', perm_views.get_perm_sales),
    url(r'^updatearticle/(?P<id>\d+)/$', perm_views.get_article_sales),
    url(r'^permautocomplete/$', perm_views.PermNameAutocomplete.as_view(), name='permname-autocomplete'),
    url(r'^sendconvention/(?P<id>\d+)$', perm_views.send_convention),

    url(r'^connexion$', utcaccounts_views.connexion_cas_api),
    url(r'^logout$', utcaccounts_views.logout),
    url(r'^getmyrights$', utcaccounts_views.get_my_rights),
    url(r'^getUserList$', utcaccounts_views.get_user_list),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += utcaccounts_urlpatterns
