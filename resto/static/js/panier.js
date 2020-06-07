$("#toggle-panier").on('click', function(event) {
	event.preventDefault();
	$("#panier").toggleClass("active");
});
$(".overlay").on('click', function(event) {
	event.preventDefault();
	$("#panier").toggleClass("active");
});