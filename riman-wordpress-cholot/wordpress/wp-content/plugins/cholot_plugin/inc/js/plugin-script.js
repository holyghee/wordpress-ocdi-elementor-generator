(function ($) {
	"use strict";
	$(window).on("load", function () {
		//for header metabox script
		if (jQuery('#cholot_header_option').val() == 'default') {
			jQuery('.cmb2-id-cholot-default-header').slideDown();
		}
		if (jQuery('#cholot_header_option').val() == 'custom') {
			jQuery('.cmb2-id-cholot-meta-choose-header').slideDown();
		}

		jQuery('#cholot_header_option').on('change', function (e) {
			if (jQuery('#cholot_header_option').val() == 'default') {
				jQuery('.cmb2-id-cholot-default-header').slideDown();
				jQuery('.cmb2-id-cholot-meta-choose-header').slideUp();
			}
			else if (jQuery('#cholot_header_option').val() == 'custom') {
				jQuery('.cmb2-id-cholot-default-header').slideUp();
				jQuery('.cmb2-id-cholot-meta-choose-header').slideDown();
			} else {
				jQuery('.cmb2-id-cholot-default-header').slideUp();
				jQuery('.cmb2-id-cholot-meta-choose-header').slideUp();
			}
		});


		//for footer metabox script
		if (jQuery('#cholot_footer_option').val() == 'default') {
			jQuery('.cmb2-id-cholot-default-footer').slideDown();
		}
		if (jQuery('#cholot_footer_option').val() == 'custom') {
			jQuery('.cmb2-id-cholot-meta-choose-footer').slideDown();
		}

		jQuery('#cholot_footer_option').on('change', function (e) {
			if (jQuery('#cholot_footer_option').val() == 'default') {
				jQuery('.cmb2-id-cholot-default-footer').slideDown();
				jQuery('.cmb2-id-cholot-meta-choose-footer').slideUp();
			}
			else if (jQuery('#cholot_footer_option').val() == 'custom') {
				jQuery('.cmb2-id-cholot-default-footer').slideUp();
				jQuery('.cmb2-id-cholot-meta-choose-footer').slideDown();
			} else {
				jQuery('.cmb2-id-cholot-default-footer').slideUp();
				jQuery('.cmb2-id-cholot-meta-choose-footer').slideUp();
			}
		});

		//for post metabox script
		//if post is gallery
		$('#post_format').on('change', function () {
			//if portfolio type the top content
			if ($('#post_format').val() == 'post_gallery') {
				$(".cmb2-id-post-gallery-setting").slideDown();
			}
			else {
				$(".cmb2-id-post-gallery-setting").slideUp();
			}
		});
		//when first load
		if ($('#post_format').val() == 'post_gallery') {
			$(".cmb2-id-post-gallery-setting").slideDown();
		}
		else {
			$(".cmb2-id-post-gallery-setting").slideUp();
		}

		//if post is slider
		$('#post_format').on('change', function () {
			//if portfolio type the top content
			if ($('#post_format').val() == 'post_slider') {
				$(".cmb2-id-post-slider-setting").slideDown();
			}
			else {
				$(".cmb2-id-post-slider-setting").slideUp();
			}
		});
		//when first load
		if ($('#post_format').val() == 'post_slider') {
			$(".cmb2-id-post-slider-setting").slideDown();
		}
		else {
			$(".cmb2-id-post-slider-setting").slideUp();
		}

		//if post is video
		$('#post_format').on('change', function () {
			//if portfolio type the top content
			if ($('#post_format').val() == 'post_video') {
				$(".cmb2-id-post-video-setting").slideDown();
			}
			else {
				$(".cmb2-id-post-video-setting").slideUp();
			}
		});
		//when first load
		if ($('#post_format').val() == 'post_video') {
			$(".cmb2-id-post-video-setting").slideDown();
		}
		else {
			$(".cmb2-id-post-video-setting").slideUp();
		}

		//if post is audio
		$('#post_format').on('change', function () {
			//if portfolio type the top content
			if ($('#post_format').val() == 'post_audio') {
				$(".cmb2-id-post-audio-setting").slideDown();
			}
			else {
				$(".cmb2-id-post-audio-setting").slideUp();
			}
		});
		//when first load
		if ($('#post_format').val() == 'post_audio') {
			$(".cmb2-id-post-audio-setting").slideDown();
		}
		else {
			$(".cmb2-id-post-audio-setting").slideUp();
		}

		//for portfolio metabox format
		$('#port_format').on('change', function () {
			//if portfolio type the top content
			if ($('#port_format').val() == 'port_standard') {
				$(".cmb2-id-top-type,.cmb2-id-port-slider-setting,.cmb2-id-port-youtube-link,.cmb2-id-port-youtube-quality,.cmb2-id-port-video-link").slideUp();
			}
			else {
				$(".cmb2-id-top-type").slideDown();
				$(".cmb2-id-port-slider-setting").slideDown();

				//top content video
				if ($('#top_type').val() == 'top_content_video') {
					$(".cmb2-id-port-video-link").slideDown();
				}
				else {
					$(".cmb2-id-port-video-link").slideUp();
				}

				//top content youtube
				if ($('#top_type').val() == 'top_content_youtube') {
					$(".cmb2-id-port-youtube-link").slideDown();
					$(".cmb2-id-port-youtube-quality").slideDown();
				}
				else {
					$(".cmb2-id-port-youtube-link").slideUp();
					$(".cmb2-id-port-youtube-quality").slideUp();
				}
			}
		});
		//when first load
		if ($('#port_format').val() == 'port_standard') {
			$(".cmb2-id-top-type").slideUp();
		}
		else {
			$(".cmb2-id-top-type").slideDown();
			$(".cmb2-id-port-slider-setting").slideDown();
		}



		//if portfolio with top content is video
		$('#top_type').on('change', function () {
			//if portfolio type the top content
			if ($('#top_type').val() == 'top_content_video') {
				$(".cmb2-id-port-video-link").slideDown();
			}
			else {
				$(".cmb2-id-port-video-link").slideUp();
			}
		});
		//when first load
		if ($('#top_type').val() == 'top_content_video' && $('#port_format').val() == 'port_two') {
			$(".cmb2-id-port-video-link").slideDown();
		}
		else {
			$(".cmb2-id-port-video-link").slideUp();
		}

		//if portfolio with top content is youtube
		$('#top_type').on('change', function () {
			//if portfolio type the top content
			if ($('#top_type').val() == 'top_content_youtube') {
				$(".cmb2-id-port-youtube-link").slideDown();
				$(".cmb2-id-port-youtube-quality").slideDown();
			}
			else {
				$(".cmb2-id-port-youtube-link").slideUp();
				$(".cmb2-id-port-youtube-quality").slideUp();
			}
		});
		//when first load
		if ($('#top_type').val() == 'top_content_youtube' && $('#port_format').val() == 'port_two') {
			$(".cmb2-id-port-youtube-link").slideDown();
			$(".cmb2-id-port-youtube-quality").slideDown();
		}
		else {
			$(".cmb2-id-port-youtube-link").slideUp();
			$(".cmb2-id-port-youtube-quality").slideUp();
		}

		//for template
		$('#page_template').on('change', function () {
			if ($('#page_template').val() == 'blank-builder.php') {
				$("#cholot_portfolio_metabox").slideUp();
			}
			else {
				$("#cholot_portfolio_metabox").slideDown();
			}
		});

		if ($('#page_template').val() == 'blank-builder.php') {
			$("#cholot_portfolio_metabox").slideUp();
		}
		else {
			$("#cholot_portfolio_metabox").slideDown();
		}

	});
})(jQuery);