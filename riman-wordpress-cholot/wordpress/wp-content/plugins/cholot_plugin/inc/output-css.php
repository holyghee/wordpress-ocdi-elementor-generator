<?php


//CSS output from customizer
function cholot_color_scheme()
{

	//color schemes
	$general = get_theme_mod('cholot_colorschemes');
	$color_general = "
	.post.sticky .content-btn:hover,.blog-slider .slide-nav:hover,.tagcloud a:hover,.searchform .searchsubmit,.post-detail::after,.content-btn:hover,.content-btn::after,
	.form-submit #submit:hover,.slide-btn,.line-subtext::before,.port-hov i,.work-content .slide-nav,
	.box-relative .sub-title::before,.portfolio-gallery a i,.wpcf7-submit,.pagination > .active > a, .pagination > .active > span, #wp-calendar caption,
	.pagination > .active > a:hover, .pagination > .active > span:hover, .pagination > .active > a:focus, .pagination > .active > span:focus,.top-title > span,.teams-btn,
	#wp-calendar td a:hover,.team-social a,.port-hover i,.hero-btn,.abtw-soc a:hover,.sk-cube-grid .sk-cube,
	.home-slider .owl-page.active,.progress-bar-cholot,.slider-btn,.port-filter a::after,.port-filter a.active,.banner-btn::after,.dbox-relative,
	.to-top:hover,.to-top::after,.blog-gallery a i,.spinner > div,#testimonial .fa,.widget-border,.port-filter a::after,.port-filter a::before,
	.to-top::after,.to-top::before,.color-bg ,.wpcf7-submit, .dark-page .wpcf7-submit,.testimonial .fa,.box-with-icon .fa,.left-box-slider .slider-line,.abtw-soc a,
	.sk-folding-cube .sk-cube:before,.img-pagination a:hover .img-pagi .fa,.slider .slick-arrow:hover,.pagi-nav-box:hover .img-pagi,.post-detail li .share-box i,
	.menu-box > div > ul.navigation > .current_page_item > a::before, .menu-box > div > ul.navigation > .current-menu-parent > a::before,.menu-box > div > ul.navigation > li > a:hover::before,
	.bread-line
	{background-color:$general;}

	a:hover,.work-content .slide-nav:hover,.wpcf7-submit:hover,.content-title span,.slider-title span,.table-content h3 > span,.box-small-icon > i,
	.blog-slider .slide-nav:hover,.blog-slider .slide-nav,.team-social a:hover,.slide-btn:hover,.hero-btn:hover,.port-filter a,.team-list-two .team-sicon li a,.blog-post-list a:hover h4,
	.personal-color,.slide-nav:hover,.tagcloud a:hover,.slider-btn:hover,.banner-btn,.team-soc a:hover,.content-box-title i,.portfolio-type-two .dbox-relative p,
	.hero-title span,.tagcloud a,.footer a,.blog-post-list a:hover h3,.abtw-soc a:hover,.slider .slick-arrow,.sidebar .widgettitle::before,.related-cat,.sidebar .widget ul li::before,.sidebar .widgettitle:after,
	.widget-about-us h3:after,#reply-title,.cholot-breadcrumbs a,.cholot-breadcrumbs,.box-crumb h1.blog-title::after
	{color:$general;}
	
	u {text-decoration-color: $general;}
	
	.p-table a ,.content-btn:hover,.blog-slider .slide-nav:hover,.work-content .slide-nav:hover,.slider-btn,.port-filter a:hover,.tagcloud a:hover
	{color:#fff;}
	.abtw-soc a:hover{background-color:#fff;}
	.wpcf7-submit:hover, .dark-page .wpcf7-submit:hover{background:transparent;}

	.blog-slider .slide-nav,.content-btn,.form-submit #submit,.form-submit #submit:hover,.blog-slider .slide-nav:hover,.cell-right-border,.cell-left-border,.wpcf7-submit, 
	.dark-page .wpcf7-submit,
	.work-content .slide-nav,.wpcf7-submit:hover,.wpcf7-submit,.pagination > .active > a, .pagination > .active > span, .pagination > .active > a:hover,.tagcloud a,.tagcloud a:hover,
	 .pagination > .active > span:hover, .pagination > .active > a:focus, .pagination > .active > span:focus,.port-filter .active,.port-filter a:hover,.port-filter a,.teams-btn,
	 .hero-btn,.abtw-soc a,.widget-about-us h3::before,.content-title::before,.to-top:hover,.content-btn:hover,.ab-bordering
	{border-color:$general;}
	";
	if ($general != '') {
		wp_add_inline_style('cholot-styles', $color_general);
	}

	//hyperlink color css
	$value = get_theme_mod('cholot_color_link');
	if ($value != '') {
		$custom_colors = "a{color:$value;}";
		wp_add_inline_style('cholot-styles', $custom_colors);
	}


	//hyperlink on hover color css
	$hover = get_theme_mod('cholot_color_link_hover');
	if ($hover != '') {
		$custom_hover = "a:hover{color:$hover;}";
		wp_add_inline_style('cholot-styles', $custom_hover);
	}



	//sticky menu background (black/all sticky background)
	$menu = get_theme_mod('cholot_all_header_bg_color');
	if ($menu != '') {
		$color_menu = ".custom-sticky-menu .is-sticky .for-sticky, .is-sticky .for-sticky{background-color: $menu;}";
		wp_add_inline_style('cholot-styles', $color_menu);
	}

	//sticky menu background (white background)
	$menu2 = get_theme_mod('cholot_white_header_bg_color');
	if ($menu2 != '') {
		$color_menu = ".white-header .is-sticky .for-sticky{background-color: $menu2;}";
		wp_add_inline_style('cholot-styles', $color_menu);
	}

	//footer background
	$footer_bg = get_theme_mod('cholot_default_footer_bg_color');
	if ($footer_bg != '') {
		$footer_color = ".footer{background-color: $footer_bg;}";
		wp_add_inline_style('cholot-styles', $footer_color);
	}
}

//CSS ouput script
add_action('wp_enqueue_scripts', 'cholot_color_scheme', 11);