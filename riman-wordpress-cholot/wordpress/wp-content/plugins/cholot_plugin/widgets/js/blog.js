(function($) {
	"use strict";

	$(window).on("load", function() {
		// makes sure the whole site is loaded
		//slider for blog slider
		$(".post-blog-slider").slick({
			autoplay: true,
			dots: false,
			arrows: false,
			speed: 800,
			fade: true,
			pauseOnHover: false,
			pauseOnFocus: false
		});
	});
})(jQuery);
