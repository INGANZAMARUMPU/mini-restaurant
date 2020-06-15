from django.urls import path, include
from rest_framework import routers
from .views import *
from .api import *

router = routers.DefaultRouter()
router.register("produit", ProduitViewset)
router.register("stock", StockViewset)
router.register("fournisseur", FournisseurViewset)
router.register("recette", RecetteViewset)
router.register("commande", CommandeViewset)
router.register("chart_menus", ChartRecetteViewset, basename='chart_menus')
router.register("chart_perso", ChartPersonnelViewset, basename='chart_perso')

urlpatterns = [
    path("api/", include(router.urls)),
	path("", Home.as_view(), name='home'),
	path("stock", StockView.as_view(), name='stock'),
	path("menus", MenuView.as_view(), name='menus'),
	path("stock/<id_produit>/in/", StockInView.as_view(), name='stock_in'),
	path("stock/<id_produit>/out/", StockOutView.as_view(), name='stock_out'),
	path("commandes", CommandeMgtView.as_view(), name='commandes'),
	# path("commandes/<sdate>/<edate>", CommandeMgtView.as_view(), name='commandes'),
	path("commandes/<id_table>", CommandeMgtView.as_view(), name='commandes'),
	path("details/<id_commande>", DetailCommandeView.as_view(), name='details'),
	path("commande/<id_table>", CommandeView.as_view(), name='commande_table'),
	path("payer/<id_commande>", PayView.as_view(), name='payer_commande'),
	path("commande/<id_table>/<id_serveur>", CommandeView.as_view(), name='commande_serveur'),
	path("serveurs", ServeurView.as_view(), name='serveurs'),
	path("login/", Connexion.as_view(), name='login'),
	path("logout/", disconnect, name='logout'),
]
