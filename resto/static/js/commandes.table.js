function resizeTable(){
	$('.scrollable-tab').each(function() {
		var p = $(this).parent();
		$(this).height(p.height() - $(this).offset().top);
	});
}
function calculateSums(){
	commande_somme = 0.0;
	commande_payee = 0.0;
	commande_reste = 0.0;
	$('.commande-item:visible').each(function() {
		commande_somme += parseFloat($(this).find('.commande-somme').text());
		commande_payee += parseFloat($(this).find('.commande-payee').text());
		commande_reste += parseFloat($(this).find('.commande-reste').text());
	});
	$("#commande-somme").text(commande_somme);
	$("#commande-payee").text(commande_payee);
	$("#commande-reste").text(commande_reste);
}
resizeTable();
calculateSums();

$(window).bind("resize", function() {
	resizeTable();
});
$('.search-form').bind("DOMChanged", function() {
    calculateSums();
});