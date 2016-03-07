from rest_framework import routers
from core import views as core_views
from facture import views as facture_views
from perm import views as perm_views


router = routers.DefaultRouter()

# Core
router.register(r'bug', core_views.BugReportViewset)
router.register(r'periodetva', core_views.PeriodeTVAViewset)

# Perms
router.register(r'perms', perm_views.PermViewSet)
router.register(r'articles', perm_views.ArticleViewSet)

# Factures
router.register(r'facturesRecues', facture_views.FactureRecueViewSet)
router.register(r'categoriesFactureRecue', facture_views.CategorieFactureRecueViewSet)
router.register(r'factureEmises', facture_views.FactureEmiseViewSet)
router.register(r'factureEmiseRows', facture_views.FactureEmiseRowViewSet)
router.register(r'cheques', facture_views.ChequeViewSet)
