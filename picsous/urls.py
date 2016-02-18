from django.conf.urls import url, include

from utcaccounts.urls import urlpatterns as utcaccounts_urlpatterns

from facture import views as facture_views
from perm import views as perm_views
from utcaccounts import views as utcaccounts_views
from router import router

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^convention/(?P<id>\d+)$', perm_views.convention_partenariat),
    url(r'^facture/(?P<id>\d+)$', facture_views.facture),
    url(r'^justificatif/(?P<id>\d+)$', perm_views.justificatif_paiement),
    url(r'^tvainfo/(?P<id>\d+)$', facture_views.tva_info),
    url(r'^createpayutcarticle/(?P<id>\d+)/$', perm_views.create_payutc_article),
    url(r'^connexion$', utcaccounts_views.connexion_cas_api),
    url(r'^getmyrights$', utcaccounts_views.get_my_rights),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += utcaccounts_urlpatterns
