$(".stock_action").on('click', function(event) {
	event.preventDefault();
	$popup_form = $("#popup-form");
	// actualiser = window.location;
	stock_id = $(this).parents('.produit-item').attr('data-id');
	url = $(this).attr('href');
	form_content = $("#form-content");
	$.ajax({
		url: url,
		dataType: "html",
	})
	.done(function(data) {
		$(form_content).html(data);
		$popup_form.addClass('active');
		$(form_content).on("submit", "#modal-form", function (e) {
			e.preventDefault();
			e.stopPropagation()
			$.ajax({
				url: url,
				type: 'POST',
				data: $(this).serialize(),
			})
			.done(function() {
				window.location = window.location;
				// window.location = window.location;
			})
			.fail(function() {
				alert("error");
			})
			.always(function() {
			});
			
		}); 
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
});


$(".overlay").on('click', function(event) {
	event.preventDefault();
	$("#popup-form").removeClass("active");
});