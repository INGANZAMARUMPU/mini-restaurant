from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict

import json
from datetime import date, timedelta

from .forms import *
from .models import *

def stringToDate(str_date:str)->datetime.date:
	if str_date:
		return datetime.datetime.strptime(str_date, "%d-%m-%Y").date()
	else:
		datetime.date.today()

class Home(LoginRequiredMixin, View):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		tables = Table.objects.all()
		return render(request, self.template_name, locals())

class StockView(LoginRequiredMixin, View):
	template_name = "stock.html"

	def get(self, request, *args, **kwargs):
		produits = Produit.objects.all()
		return render(request, self.template_name, locals())

class MenuView(LoginRequiredMixin, View):
	template_name = "menus.html"

	def get(self, request, *args, **kwargs):
		recettes = Recette.objects.all()
		return render(request, self.template_name, locals())

class PersonnelView(LoginRequiredMixin, View):
	template_name = "personnel.html"

	def get(self, request, *args, **kwargs):
		personnel = User.objects.all()
		return render(request, self.template_name, locals())

class ServeurView(LoginRequiredMixin, View):
	template_name = "serveur.html"

	def get(self, request, *args, **kwargs):
		serveurs = Serveur.objects.all()
		return render(request, self.template_name, locals())

class CommandeMgtView(LoginRequiredMixin, View):
	template_name = "commandes.html"

	# def get(self, request, sdate=None, edate=None, *args, **kwargs):
	def get(self, request, *args, **kwargs):
		today = date.today()
		date_form = DateForm()
		tomorrow = today - timedelta(days=1)
		commandes = Commande.objects.filter(date__gte=tomorrow, date__lte=today)
		return render(request, self.template_name, locals())

	def post(self, request, *args, **kwargs):
		date_form = DateForm(request.POST)
		
		if date_form.is_valid():
			sdate = date_form.cleaned_data["sdate"]
			edate = date_form.cleaned_data["edate"]
		# today = date.today()
		# sdate = today.replace(day = 1)
		# edate = today.replace(month=(today.month+1)%12, day=1) - timedelta(days=1)
		# tomorrow = today - timedelta(days=1)
		commandes = Commande.objects.filter(date__gte=sdate, date__lte=edate)
		return render(request, self.template_name, locals())

class StockInView(LoginRequiredMixin, View):
	template_name = "forms.html"

	def get(self, request, id_produit,*args, **kwargs):
		form = InStockForm(id_produit)
		return render(request, self.template_name, locals())

	def post(self, request, id_produit, *args, **kwargs):
		form = InStockForm(id_produit, request.POST)
		if(form.is_valid):
			stock = form.save(commit=False)
			stock.produit=stock.offre.produit
			stock.save()
		return render(request, self.template_name, locals())

class PayView(LoginRequiredMixin, View):
	template_name = "payment_forms.html"

	def get(self, request, id_commande,*args, **kwargs):
		commande = get_object_or_404(Commande, id=id_commande)
		form = PayForm(instance=commande)
		return render(request, self.template_name, locals())

	def post(self, request, id_commande, *args, **kwargs):
		commande = get_object_or_404(Commande, id=id_commande)
		form = PayForm(request.POST, instance=commande)
		if(form.is_valid):
			new_commande = form.save(commit=False)
			if new_commande.payee >= commande.a_payer:
				new_commande.payee = commande.a_payer
				new_commande.save()
		return render(request, self.template_name, locals())

class StockOutView(LoginRequiredMixin, View):
	template_name = "forms.html"

	def get(self, request, id_produit, *args, **kwargs):
		form = OutStockForm(id_produit)
		return render(request, self.template_name, locals())

	def post(self, request, id_produit, *args, **kwargs):
		form = OutStockForm(id_produit, request.POST)
		if(form.is_valid()):
			form.save()
		return render(request, self.template_name, locals())

class CommandeView(LoginRequiredMixin, View):
	template_name = "commande_serveurs.html"

	def get(self, request, id_table=None, id_serveur=None, *args, **kwargs):
		if(id_table and id_serveur):
			recettes = Recette.objects.all()
			return render(request, "commande_recettes.html", locals())

		elif id_table:
			serveurs = Serveur.objects.all()
			return render(request, "commande_serveurs.html", locals())

		else:
			commandes = Commande.objects.all()
			return render(request, self.template_name, locals())

	def post(self, request, id_table, id_serveur, *args, **kwargs):
		table = Table.objects.get(id = id_table)
		serveur = Serveur.objects.get(id = id_serveur)
		commande = Commande.objects.get_or_create(table=table,\
	 		serveur=serveur, a_payer=0)[0]
		facture = {}
		facture["serveur"] = str(commande.serveur)
		facture["id"] = commande.id
		facture["date"] = commande.date
		facture["table"] = str(commande.table)
		facture["caissier"] = request.user.first_name+" "+request.user.last_name
		facture["factures"] = []
		for id_recette, details in json.loads(request.body).items():
			recette = Recette.objects.get(id=id_recette)
			detail_commande = DetailCommande(recette=recette, commande=commande,\
				quantite=details["quantite"])
			detail_commande.save()
			details["id"] = id_recette
			details["total"] = float(details["quantite"])*float(details["prix"])
			facture["factures"].append(details)
		facture["total"] = commande.a_payer
		return JsonResponse(facture)

class DetailCommandeView(LoginRequiredMixin, View):
	template_name = "details_commande.html"

	def get(self, request, id_commande, *args, **kwargs):
		commande = Commande.objects.get(id=id_commande)
		details = DetailCommande.objects.filter(commande=commande)
		return render(request, self.template_name, locals())

	def post(self, request, id_commande, *args, **kwargs):
		commande = Commande.objects.get(id=id_commande)
		if commande:
			commande.delete()
		return render(request, self.template_name, locals())	

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
