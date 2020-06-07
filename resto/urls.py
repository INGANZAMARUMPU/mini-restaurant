from django.urls import path, include
from .views import *

urlpatterns = [
	path("", Home.as_view(), name='home'),
	path("stock", StockView.as_view(), name='stock'),
	path("menus", MenuView.as_view(), name='menus'),
	path("commandes", Home.as_view(), name='commandes'),
	path("commande/<id_table>", CommandeView.as_view(), name='commande_table'),
	path("commande/<id_table>/<id_serveur>", CommandeView.as_view(), name='commande_serveur'),
	path("personnel", PersonnelView.as_view(), name='personnel'),
	path("login/", Connexion.as_view(), name='login'),
	path("logout/", disconnect, name='logout'),
]
