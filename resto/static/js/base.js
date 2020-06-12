$(".toggle-submenu").hover(function() {
	$(this).find('.submenu').show();
}, function() {
	$(this).find('.submenu').hide();
});

function search(search_widget, class_name){
	search_widget = '.'+search_widget;
	class_name = '.'+class_name;
	$text_field = $(search_widget).find('input');

	$text_field.keyup(function(event) {
		keyword = $(this).val().toLowerCase();
		for(var item of $(class_name)){
			content = $(item).text().trim().toLowerCase();
			if(content.includes(keyword)){
		      $(item).show();
		    }else{
		      $(item).hide();
		    }
		}
	});
	$(search_widget).on('reset', function(event) {
		$(class_name).show();
	});
}