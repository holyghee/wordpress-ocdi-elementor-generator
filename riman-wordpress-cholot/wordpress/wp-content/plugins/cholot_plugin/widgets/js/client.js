(function($) {
	"use strict";

	//slider client
	$(".client-slider").slick({
		slidesToShow: 6,
		slidesToScroll: 1,
		arrows: false,
		autoplay: true,
		responsive: [
			{
				breakpoint: 1024,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 3,
					infinite: true,
					dots: false
				}
			},
			{
				breakpoint: 600,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 2
				}
			},
			{
				breakpoint: 480,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 1
				}
			}
		]
	});
})(jQuery);
