from django.contrib import admin
from .models import *

class PersonnelAdmin(admin.ModelAdmin):
	list_display = ("user", "tel", "avatar")
	list_filter = ("user", "tel")
	search_field = ("user", "tel")
	ordering = ("user", "tel")

class ProduitAdmin(admin.ModelAdmin):
	list_display = ("nom", "unite", "unite_sortant")
	list_filter = ("nom", "unite", "unite_sortant")
	search_field = ("nom", "unite", "unite_sortant")
	ordering = ("nom", "unite", "unite_sortant")

class OffreAdmin(admin.ModelAdmin):
	list_display = ('produit', 'fournisseur', "prix")
	list_filter = ('produit', 'fournisseur', "prix")
	search_field = ('produit', 'fournisseur', "prix")
	ordering = ('produit', 'fournisseur', "prix")

class StockAdmin(admin.ModelAdmin):
	list_display = ("produit", "quantite", "offre", "personnel", "date", "expiration_date", "is_valid")
	list_filter = ("produit", "quantite", "offre", "personnel", "date", "expiration_date", "is_valid")
	search_field = ("produit", "quantite", "offre", "personnel", "date", "expiration_date", "is_valid")
	ordering = ("produit", "quantite", "offre", "personnel", "date", "expiration_date", "is_valid")

class FournisseurAdmin(admin.ModelAdmin):
	list_display = ('nom', 'adresse', 'tel')
	list_filter = ('nom', 'adresse', 'tel')
	search_field = ('nom', 'adresse', 'tel')
	ordering = ('nom', 'adresse', 'tel')

class RecetteAdmin(admin.ModelAdmin):
	list_display = ("nom", "image", "prix", "details")
	list_filter = ("nom", "image", "prix", "details")
	search_field = ("nom", "image", "prix", "details")
	ordering = ("nom", "image", "prix", "details")

class CommandeAdmin(admin.ModelAdmin):
	list_display = ("table", "tel", "date", "a_payer", "payee", "reste")
	list_filter = ("table", "tel", "date", "a_payer", "payee", "reste")
	search_field = ("table", "tel", "date", "a_payer", "payee", "reste")
	ordering = ("table", "tel", "date", "a_payer", "payee", "reste")

class PaiementAdmin(admin.ModelAdmin):
	list_display = ("commande","somme","date")
	list_filter = ("commande","somme","date")
	search_field = ("commande","somme","date")
	ordering = ("commande","somme","date")

class PlaceAdmin(admin.ModelAdmin):
	list_display = ("nom",)
	list_filter = ("nom",)
	search_field = ("nom",)
	ordering = ("nom",)

class DetailCommandeAdmin(admin.ModelAdmin):
	list_display = ("recette", "commande", "quantite", "somme", "date")
	list_filter = ("recette", "commande", "quantite", "somme", "date")
	search_field = ("recette", "commande", "quantite", "somme", "date")
	ordering = ("recette", "commande", "quantite", "somme", "date")

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Recette, RecetteAdmin)
admin.site.register(DetailCommande, DetailCommandeAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Offre, OffreAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Table)
