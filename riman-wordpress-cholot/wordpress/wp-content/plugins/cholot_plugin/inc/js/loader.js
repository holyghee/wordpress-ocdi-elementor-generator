(function ($) {
	"use strict";
	$(window).on("load", function () {
		// makes sure the whole site is loaded
		//preloader
		$("#status")
			.delay(100)
			.fadeOut('fast'); // will first fade out the loading animation
		$("#preloader")
			.delay(300)
			.slideUp(); // will fade out the white DIV that covers the website.
	});
})(jQuery);