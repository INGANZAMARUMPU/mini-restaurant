from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

import json

from .forms import *
from .models import *

class Home(View, LoginRequiredMixin):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		tables = Table.objects.all()
		return render(request, self.template_name, locals())

class StockView(View, LoginRequiredMixin):
	template_name = "stock.html"

	def get(self, request, *args, **kwargs):
		produits = Produit.objects.all()
		return render(request, self.template_name, locals())

class MenuView(View, LoginRequiredMixin):
	template_name = "menus.html"

	def get(self, request, *args, **kwargs):
		recettes = Recette.objects.all()
		return render(request, self.template_name, locals())

class PersonnelView(View, LoginRequiredMixin):
	template_name = "personnel.html"

	def get(self, request, *args, **kwargs):
		serveurs = User.objects.all()
		return render(request, self.template_name, locals())

class CommandeMgtView(View, LoginRequiredMixin):
	template_name = "commandes.html"

	def get(self, request, *args, **kwargs):
		commandes = Commande.objects.all()
		return render(request, self.template_name, locals())

class StockInView(View):
	template_name = "forms.html"

	def get(self, request, id_produit,*args, **kwargs):
		form = InStockForm(id_produit)
		return render(request, self.template_name, locals())

	def post(self, request, id_produit, *args, **kwargs):
		form = InStockForm(id_produit, request.POST)
		if(form.is_valid):
			data = form.save(commit=False)
			produit = Produit.objects.get(id = id_produit)
			Stock(produit=produit, quantite=data.quantite,\
				offre=data.offre, expiration=data.expiration).save()
		return render(request, self.template_name, locals())

class StockOutView(View):
	template_name = "forms.html"

	def get(self, request, id_produit, *args, **kwargs):
		form = OutStockForm()
		return render(request, self.template_name, locals())

	def post(self, request, id_produit, *args, **kwargs):
		import math
		form = OutStockForm(request.POST)
		if(form.is_valid):
			data = form.save(commit=False)
			produit = Produit.objects.get(id = id_produit)
			Stock(produit=produit, motif = data.motif,\
				quantite=-math.sqrt(float(data.quantite)**2)).save()
		return render(request, self.template_name, locals())

class CommandeView(View, LoginRequiredMixin):
	template_name = "commande_serveurs.html"

	def get(self, request, id_table=None, id_serveur=None, *args, **kwargs):
		if(id_table and id_serveur):
			recettes = Recette.objects.all()
			return render(request, "commande_recettes.html", locals())

		elif id_table:
			serveurs = Personnel.objects.all()
			return render(request, "commande_serveurs.html", locals())

		else:
			commandes = Commande.objects.all()
			return render(request, self.template_name, locals())

	def post(self, request, id_table, id_serveur, *args, **kwargs):
		commande = Commande.objects.get_or_create(table=id_table,\
	 		serveur=id_serveur, a_payer=0)[0]
		for id_recette, details in json.loads(request.body).items():
			print(id_recette, details)
			recette = Recette.objects.get(id=id_recette)
			DetailCommande(recette=recette, commande=commande,\
				quantite=details["quantite"]).save()
		return JsonResponse({"message":"good"})
		

def disconnect(request):
	show_hidden = "hidden"
	logout(request)
	return redirect("login")

class Connexion(View):
	template_name = 'login.html'
	next_p = "home"

	def get(self, request, *args, **kwargs):
		form = ConnexionForm()
		try:
			self.next_p = request.GET["next"]
		except:
			print
		return render(request, self.template_name, locals())

	def post(self, request, *args, **kwargs):
		form = ConnexionForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:  # Si l'objet renvoyé n'est pas None
				login(request, user)
				messages.success(request, "You're now connected!")
				return redirect(self.next_p)
			else:
				messages.error(request, "logins incorrect!")
		return render(request, self.template_name, locals())
