from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import *
from .serializers import *

class ProduitViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Produit.objects.all()
	serializer_class = ProduitSerializer

class StockViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Stock.objects.all()
	serializer_class = StockSerializer

	@action(methods=['GET'], detail=False,
		url_path=r'quantite/(?P<produit_id>[0-9]+)',
		url_name="quantite_total")
	def quantiteTotal(self, request, produit_id):
		produit = Produit.objects.get(id=produit_id)
		return Response({'quantite':produit.quantiteEnStock()})

class FournisseurViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Fournisseur.objects.all()
	serializer_class = FournisseurSerializer

class RecetteViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Recette.objects.all()
	serializer_class = RecetteSerializer

class CommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Commande.objects.all()
	serializer_class = CommandeSerializer
