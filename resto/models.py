from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

class Personnel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('tel', 'user')

	def __str__(self):
		string = self.user.first_name+self.user.last_name
		string = string if string else self.user.username
		return f"{string}"

class Table(models.Model):
	number = models.IntegerField()

	def __str__(self):
		return f"Table {self.number}"

class Produit(models.Model):
	nom = models.CharField(max_length=64, unique=True)
	unite = models.CharField(max_length=64, verbose_name='unité de mesure')
	unite_sortant = models.CharField(max_length=64, null=True,blank=True)
	rapport = models.FloatField(default=1)

	def __str__(self):
		return self.nom

	def quantiteEnStock(self):
		stocks = Stock.objects.filter(produit=self, is_valid=True)
		quantite = stocks.aggregate(Sum('quantite'))['quantite__sum']
		try:
			return int(quantite)
		except:
			return 0

	class Meta:
		ordering = ["nom"]

class Stock(models.Model):
	produit = models.ForeignKey("Produit", on_delete=models.CASCADE)
	offre = models.ForeignKey("Offre", blank=True, null=True, on_delete=models.SET_NULL)
	quantite = models.FloatField()
	date = models.DateField(blank=True, default=timezone.now)
	expiration = models.PositiveIntegerField(null=True, verbose_name="délais de validité(en jours)")
	expiration_date = models.DateField(editable=False, null=True)
	personnel = models.ForeignKey("Personnel", null=True, on_delete=models.SET_NULL)
	is_valid = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.expiration:
			self.expiration_date=self.date+timedelta(days=self.expiration)
		super(Stock, self).save(*args, **kwargs)

	class Meta:
		ordering = ["produit"]

class Offre(models.Model):
	produit = models.ForeignKey("Produit", null=True, on_delete=models.SET_NULL)
	fournisseur = models.ForeignKey("Fournisseur", null=True, on_delete=models.SET_NULL)
	prix = models.FloatField()

	def __str__(self):
		return f"{self.produit.nom} - {self.fournisseur} - {self.prix}"

	class Meta:
		unique_together = ('produit', 'fournisseur', 'prix')

class Fournisseur(models.Model):
	nom = models.CharField(verbose_name='nom et prenom', max_length=64)
	adresse = models.CharField(max_length=64)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('adresse', 'tel')
	def __str__(self):
		return f"{self.nom}"

class Recette(models.Model):
	nom = models.CharField(max_length=64)
	prix = models.PositiveIntegerField()
	image = models.ImageField(upload_to="recettes/")
	disponible = models.BooleanField(default=True)
	details = models.URLField(null=True, blank=True)

	def __str__(self):
		return f"{self.nom} à {self.prix}"

class DetailCommande(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.CASCADE, related_name='details')
	recette = models.ForeignKey("Recette", null=True, on_delete=models.SET_NULL)
	quantite = models.PositiveIntegerField(default=1)
	somme = models.PositiveIntegerField(blank=True, verbose_name='à payer')
	date = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		self.somme = self.recette.prix*self.quantite
		super(DetailCommande, self).save(*args, **kwargs)

	class Meta:
		unique_together = ('commande','recette')
		ordering = ['date']
			
	def __str__(self):
		return f"{self.recette}"

class Commande(models.Model):
	table = models.ForeignKey(Table, default=1, on_delete=models.SET_DEFAULT)
	tel = models.CharField(verbose_name='numero de télephone', blank=True, default=0, max_length=24)
	date = models.DateField(blank=True, default=timezone.now)
	a_payer = models.FloatField(default=0, blank=True)
	payee = models.FloatField(default=0, blank=True)
	reste = models.FloatField(default=0, blank=True)
	serveur = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

	def save(self, *args, **kwargs):
		self.reste = self.a_payer-self.payee
		super(Commande, self).save(*args, **kwargs)

	def paniers(self):
		return Panier.objects.filter(commande=self)

class Paiement(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.SET_NULL)
	somme = models.PositiveIntegerField(verbose_name='somme payée', default=0)
	date = models.DateField(blank=True, default=timezone.now)

	def save(self, *args, **kwargs):
		commande = self.commande
		super(Paiement, self).save(*args, **kwargs)
		# paiements = Paiement.objects.filter(commande=commande).aggregate(Sum("somme"))["somme__sum"]
		# commande.payee = paiements
		commande.payee += self.somme
		commande.reste = commande.a_payer-paiements
		commande.save()