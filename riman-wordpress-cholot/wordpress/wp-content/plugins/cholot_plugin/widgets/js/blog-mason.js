(function($) {
	"use strict";
	$(window).on("load", function() {
		// makes sure the whole site is loaded

		$(".blog-body").each(function() {
			$(this).isotope();
		});
		//make sure the site ready
		setTimeout(function() {
			$(".blog-body").each(function() {
				$(this).isotope();
			});
		}, 500);
	});
})(jQuery);
