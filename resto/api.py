from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Count

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

class ChartRecetteViewset(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]

	@action(methods=['GET'], detail=False, url_path=r'detail',url_name="detail")
	def menuDetail(self, request):
		details = DetailCommande.objects.values('recette__nom').\
			order_by('recette').annotate(total=Sum('quantite'))
		# serializer = DetailCommandeSerializer(details, many=True)
		return Response(details)

class ChartPersonnelViewset(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]

	@action(methods=['GET'], detail=False, url_path=r'service',url_name="service")
	def menuDetail(self, request):
		details = Commande.objects.values('serveur', 'serveur__username').\
			order_by('serveur').annotate(commandes=Count('id', distinct=True))
		# serializer = DetailCommandeSerializer(details, many=True)
		return Response(details)