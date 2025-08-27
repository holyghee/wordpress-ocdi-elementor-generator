(function($) {
	"use strict";

	$.fn.changeElementType = function(newType) {
		var attrs = {};
		if (!(this[0] && this[0].attributes)) return;

		$.each(this[0].attributes, function(idx, attr) {
			attrs[attr.nodeName] = attr.nodeValue;
		});
		this.replaceWith(function() {
			return $("<" + newType + "/>", attrs).append($(this).contents());
		});
	};

	$(window).on("load", function() {
		// makes sure the whole site is loaded

		//sticky navigation
		$(".for-sticky").sticky({
			topSpacing: 0
		});

		//change image into  background in next/prev post
		$(".pagimgbox").each(function() {
			var src = $(this)
				.children("img")
				.attr("src");
			if ($(this).children("img").length) {
				$(this).css("background-image", "url(" + src + "");
			}
		});

		if (Modernizr.touch) {
			//add class on touch device
			$("body").addClass("no-para");
		}

		//for slick navigation
		$(".home-nav,.menu-box>.menu>ul,.cholot-nav").slicknav({
			label: "",
			appendTo: ".mobile-menu-container",
			closedSymbol: "+",
			openedSymbol: "-",
			allowParentLinks: true
		});
	});

	// script popup image
	$(".popup-img").magnificPopup({
		type: "image"
	});

	// script popup image
	$(".blog-popup-img").magnificPopup({
		type: "image",
		gallery: {
			enabled: true
		}
	});

	// Video responsive
	$("body").fitVids();

	//script for navigation(superfish)
	$(".menu-box ul").superfish({
		delay: 400, //delay on mouseout
		animation: {
			opacity: "show",
			height: "show"
		}, // fade-in and slide-down animation
		animationOut: {
			opacity: "hide",
			height: "hide"
		},
		speed: 200, //  animation speed
		speedOut: 200,
		autoArrows: false // disable generation of arrow mark-up
	});

	//add image mask
	$(".bg-with-mask").each(function() {
		$(this).append('<div class="slider-mask"></div>');
	});

	//slider for blog slider
	$(".blog-slider").slick({
		autoplay: true,
		dots: false,
		arrows: false,
		speed: 800,
		fade: true,
		pauseOnHover: false,
		pauseOnFocus: false
	});

	//replace the data-background into background image
	$(".blog-img-bg").each(function() {
		var imG = $(this).data("background");
		$(this).css("background-image", "url('" + imG + "') ");
	});

	//remove footer empty footer icon
	if ($(".footer-icon").has("li").length == 0) {
		$(".footer-icon").remove();
	}

	//change h5 class for custom footer
	$(".cholot-custom-footer div[class*='elementor-widget-wp-'] h5").each(
		function() {
			$(this).addClass("elementor-heading-title");
		}
	);

	//sticky custom header
	$(".custom-sticky-menu .elementor-section:has(.white-header.no-bg)")
		.first()
		.addClass("for-sticky");

	//adding/removing sticky menu class
	$(".for-sticky").on("sticky-start", function() {
		$(this).addClass("cholot-sticky-menu");
		$(this)
			.find(".cholot-nav,.box-mobile")
			.addClass("cholot-stick");
	});
	$(".for-sticky").on("sticky-end", function() {
		$(this).removeClass("cholot-sticky-menu");
		$(this)
			.find(".cholot-nav,.box-mobile")
			.removeClass("cholot-stick");
	});

	//add class for hovering team & hovering icon
	$(
		".elementor-widget-cholot-team-hover,.elementor-widget-cholot-texticon-hover"
	).each(function() {
		$(this)
			.closest(".elementor-column-wrap")
			.addClass("hovering");
	});
})(jQuery);
