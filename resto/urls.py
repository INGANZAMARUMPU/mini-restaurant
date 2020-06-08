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

urlpatterns = [
    path("api/", include(router.urls)),
	path("", Home.as_view(), name='home'),
	path("stock", StockView.as_view(), name='stock'),
	path("menus", MenuView.as_view(), name='menus'),
	path("stock_in/<id_produit>", StockInView.as_view(), name='stock_in'),
	path("stock_out/<id_produit>", StockOutView.as_view(), name='stock_out'),
	path("commandes", CommandeMgtView.as_view(), name='commandes'),
	path("commande/<id_table>", CommandeView.as_view(), name='commande_table'),
	path("commande/<id_table>/<id_serveur>", CommandeView.as_view(), name='commande_serveur'),
	path("personnel", PersonnelView.as_view(), name='personnel'),
	path("login/", Connexion.as_view(), name='login'),
	path("logout/", disconnect, name='logout'),
]
