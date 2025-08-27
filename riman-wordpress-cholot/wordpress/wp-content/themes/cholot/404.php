<?php
get_header();

//custom header
if (class_exists('Kirki')) {
	do_action('cholot-custom-header', 'cholot_header_start');
} else { ?>

<!--Fall back if no kirki plugin installed-->
<!--HOME START-->
<div class="default-header clearfix">
    <!--HEADER START-->
    <?php get_template_part('loop/menu', 'normal'); ?>
    <!--HEADER END-->
</div>
<!--/home end-->
<!--HOME END-->

<?php } ?>

<!--breadcrumb if available-->
<?php if (function_exists('cholot_breadcrumb')) { ?>
<div class="box-crumb clearfix">
    <div class="slider-mask"></div>
    <div class="container">


        <?php if (function_exists('cholot_breadcrumb')) {
				cholot_breadcrumb();
			} ?>
        <h1 class="blog-title"><?php esc_html_e('Page not found', 'cholot'); ?></h1>
        <div class="bread-line"></div>


    </div>

</div>
<?php } ?>

<div class="clearfix content page-content-wrapper">
    <div class="container-fluid error-container">
        <div class="row">
            <div class="col-md-4 error-col">
                <h2 class="error-title"><?php esc_html_e('404', 'cholot'); ?></h2>
            </div>
            <div class="col-md-8 error-col">
                <p class="error-bigtext"><?php esc_html_e('Oops..', 'cholot') ?></p>
                <p class="error-text"><?php esc_html_e('Page not found!', 'cholot') ?></p>
                <p><?php esc_html_e('We could not find that page. If you entered a web address please check it was correct.', 'cholot') ?>
                </p>
                <a class="content-btn" href="<?php echo esc_url(home_url('/')); ?>">
                    <?php echo esc_html__('Back to Homepage', 'cholot') ?>
                </a>
            </div>

        </div>
        <!--/.row-->
    </div>
    <!--/.container-->
</div>
<!--/.content-->


<?php //custom footer
//custom footer
if (class_exists('Kirki')) {
	do_action('cholot-custom-footer', 'cholot_footer_start');
} else {
	//fallback if no kirki installed
	get_template_part('loop/bottom', 'footer');
}

get_footer(); ?>