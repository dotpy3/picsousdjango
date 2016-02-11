from django.conf.urls import url, include
from facture import views as facture_views
from perm import views as perm_views
from rest_framework import routers

from utcaccounts.urls import urlpatterns as utcaccounts_urlpatterns

router = routers.DefaultRouter()
router.register(r'perms', perm_views.PermViewSet)
router.register(r'articles', perm_views.ArticleViewSet)
router.register(r'updateArticle', perm_views.UpdateArticleViewSet)
router.register(r'facturesRecues', facture_views.FactureRecueViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += utcaccounts_urlpatterns
