$(".stock_action").on('click', function(event) {
	event.preventDefault();
	$popup_form = $("#popup-form");
	if(!($popup_form.hasClass('active'))){
		$popup_form.addClass('active');
		form_content = $("#form-content");
		// $form_content.load($(this).attr('href'));
		$(form_content).load($(this).attr('href'));
		
		$(form_content).on("submit", "#modal-form", function (e) {
			e.preventDefault();
			$.ajax({
				url: $(this).attr('action'),
				type: 'POST',
				data: $(this).serialize(),
			})
			.done(function() {
				alert("success");
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