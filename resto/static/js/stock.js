$(".stock_action").on('click', function(event) {
	event.preventDefault();
	$popup_form = $("#popup-form");
	// actualiser = window.location;
	stock_id = $(this).parents('.produit-item').attr('data-id');
	if(!($popup_form.hasClass('active'))){
		$popup_form.addClass('active');
		form_content = $("#form-content");
		url = $(this).attr('href');
		$(form_content).load(url);
		
		$(form_content).on("submit", "#modal-form", function (e) {
			e.preventDefault();
			$.ajax({
				url: url,
				type: 'POST',
				data: $(this).serialize(),
			})
			.done(function() {
				alert("success");
				window.location = window.location;
				// window.location = window.location;
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
			});
			
		}); 

	}
});


$(".overlay").on('click', function(event) {
	event.preventDefault();
	$("#popup-form").toggleClass("active");
});