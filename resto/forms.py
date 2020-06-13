from .models import *
from django import forms

class ConnexionForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={'placeholder':'Username ', 'class':'input'}),
		# label=""
	)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={'placeholder':'Password ', 'class':'input', 'type':'password'}
		),
		# label=""
	)

class InStockForm(forms.ModelForm):
	offre = forms.ModelChoiceField(
		widget = forms.Select(
			attrs={'placeholder':'offre','class':'input'}),
		queryset = Offre.objects.all())
	quantite = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'quantite','class':'input'}))
	expiration = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'délais de validité(en jours)',
					'class':'input'}))
	class Meta:
		model = Stock
		fields = ("offre", "quantite", "expiration")

	def __init__(self, produit_id, *args, **kwargs):
		self.base_fields["offre"].queryset = Offre.objects.filter(produit=produit_id)
		super(InStockForm, self).__init__(*args, **kwargs)

MOTIF_CHOICES = ( 
    ("vers_cuisine", "vers cuisine"), 
    ("vers_caisse", "vers caisse"), 
    ("perime", "perimé"),
)

class PayForm(forms.ModelForm):
	payee = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'la somme payée','class':'input', 'id':"saisies"}),
		label='la somme payée'
		)
	class Meta:
		model = Commande
		fields = ("payee",)

class OutStockForm(forms.ModelForm):
	quantite = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'quantite','class':'input'}))

	motif = forms.ChoiceField(
		widget=forms.Select(
			attrs={'placeholder':'motif ', 'class':'input'}),
		# label="motif"
		choices=MOTIF_CHOICES
	)

	class Meta:
		model = Stock
		fields = ("quantite", "motif")