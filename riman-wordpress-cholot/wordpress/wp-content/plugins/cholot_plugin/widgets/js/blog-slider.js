(function($) {
	"use strict";
	// makes sure the whole site is loaded
	$(window).on("load", function() {
		//slider client slider
		$(".post-slider").each(function() {
			var $slide = $(this).data("slide");
			var $tabs = $(this).data("slide-tablet");
			var $mobile = $(this).data("slide-mobile");
			$(this).slick({
				slidesToShow: $slide,
				slidesToScroll: 1,
				arrows: false,
				autoplay: true,
				responsive: [
					{
						breakpoint: 1024,
						settings: {
							slidesToShow: $tabs,
							slidesToScroll: 1
						}
					},
					{
						breakpoint: 480,
						settings: {
							slidesToShow: $mobile,
							slidesToScroll: 1
						}
					}
				]
			});
		});
	});
})(jQuery);
