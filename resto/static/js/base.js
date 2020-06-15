$(".toggle-submenu").hover(function() {
	$(this).find('.submenu').show();
}, function() {
	$(this).find('.submenu').hide();
});

function search(search_widget, class_name){
	search_widget = '.'+search_widget;
	class_name = '.'+class_name;
	dom_changed = false;
	$text_field = $(search_widget).find('input');

	$text_field.keyup(function(event) {
		keyword = $(this).val().toLowerCase();
		for(var item of $(class_name)){
			content = $(item).text().trim().toLowerCase();
			if(content.includes(keyword)){
				if($(item).is(':hidden')){
					$(item).show();
					dom_changed = true;
				}
		    }else{
				if($(item).is(':visible')){
					$(item).hide();
					dom_changed = true;
				}
		    }
		}
		if(dom_changed){
			$(this).trigger('DOMChanged');
			dom_changed = false;
		}
	});
	$(search_widget).on('reset', function(event) {
		$(class_name).show();
	});
}
$(".url_button").off('click').on('click', function(event) {
	event.preventDefault();
	$popup_form = $("#popup-form");
	url = $(this).attr('href');
	form_content = $("#form-content");
	$.ajax({
		url: url,
		dataType: "html"
	})
	.done(function(data) {
		$(form_content).html(data);
		$popup_form.addClass('active');
		$(form_content).find("form").on("submit",function (e) {
			e.preventDefault();
			e.stopPropagation();
			$.ajax({
				url: url,
				type: 'POST',
				data: $(this).serialize(),
			})
			.done(function() {
				window.location = window.location;
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

$(".popup").on('mousedown', function(event) {
	if(!event.target.matches('.popup-body, .popup-body *')){
		$(".popup").removeClass('active');
	}
});