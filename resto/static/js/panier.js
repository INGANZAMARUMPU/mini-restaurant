var panier = {};

function templatePanier(id, name, prix, quantite){
	total=prix*quantite;
	return`
	<tr class="panier-item" data-id="`+id+`">
		<td class="panier-name">`+name+`</td>
		<td class="panier-prix">`+prix+`</td>
		<td class="panier-quantite">`+quantite+`</td>
		<td class="panier-total">`+total+`</td>
		<td><button class="panier_moins">-</button></td>
		<td><button class="panier_plus">+</button></td>
	</tr>
	`
}
$("#panier").on('click', '.panier_plus', function(event) {
	event.preventDefault();
	$item = $(this).parents(".panier-item");
	$quantite = $item.find(".panier-quantite");
	quantite = parseInt($quantite.text())+1;
	$total = $item.find(".panier-total");
	prix = parseInt($item.find(".panier-prix").text());
	$quantite.text(quantite);
	$total.text(quantite*prix);
	calculateTotal();
});

$("#panier").on('click', '.panier_moins', function(event) {
	event.preventDefault();
	$item = $(this).parents(".panier-item");
	$quantite = $item.find(".panier-quantite");
	quantite = parseInt($quantite.text())-1;
	if(quantite>0){
		$total = $item.find(".panier-total");
		prix = parseInt($item.find(".panier-prix").text());
		$quantite.text(quantite);
		$total.text(quantite*prix);
	}else{
		$item.remove();
	}
	calculateTotal();
});

$("#toggle-panier").on('click', function(event) {
	event.preventDefault();
	$panier = $("#panier");
	if(!($panier.hasClass('active'))){
		$panier.find('tbody').empty();
		for(var [name, item] of  Object.entries(panier)){
			$panier.find('tbody').append(templatePanier(item.id, name,item.prix,item.quantite));
		}
		$panier.addClass('active');
	}
	calculateTotal();
});
$(".overlay").on('click', function(event) {
	event.preventDefault();
	$("#panier").toggleClass("active");
});

$recette_plus = $(".recette_plus");
$recette_moins = $(".recette_moins");

$recette_plus.on('click', function(event) {
	$recette = $(this).parents(".recette");
	$recette_qtt = $recette.find(".recette_qtt");
	recette_qtt = parseInt($recette_qtt.text())+1;
	recette_id = $recette.attr('data-id');
	recette_name = $recette.find(".name").text();
	recette_prix = $recette.find(".prix").text();
	item = {"id":recette_id, "quantite":recette_qtt, "prix":recette_prix};
	$recette_qtt.text(recette_qtt);
	panier[recette_name] = item;
});

$recette_moins.on('click', function(event) {
	$recette = $(this).parents(".recette");
	$recette_qtt = $recette.find(".recette_qtt");
	recette_qtt = parseInt($recette_qtt.text())-1;
	if(recette_qtt>0){
		recette_id = $recette.attr('data-id');
		recette_name = $recette.find(".name").text();
		recette_prix = $recette.find(".prix").text();
		item = {"id":recette_id, "quantite":recette_qtt, "prix":recette_prix};
		
		$recette_qtt.text(recette_qtt);
		panier[recette_name] = item;
	}else{
		$recette_qtt.text(0);
		recette_name = $recette.find(".name").text();
		delete(panier[recette_name]);
	}
});

function calculateTotal(){
	$panier = $(".panier-item");
	total = 0;
	for(let panier_item of $panier){
		total += parseInt($(panier_item).find('.panier-total').text());
	}
	$("#total").text(total)
}