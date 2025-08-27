<?php
//function for custom footer
function cholot_footer_start()
{
	if (is_singular()) { //if single page/post
		global $post;
		if (get_post_meta(get_the_ID(), 'cholot_footer_option', true) == 'custom' && get_post_meta(get_the_ID(), 'cholot_meta_choose_footer', true)) {
			$footer_id =  get_post_meta(get_the_ID(), 'cholot_meta_choose_footer', true);

			$cholot_footer = new WP_Query(array(
				'posts_per_page'   => 1,
				'post_type' =>  'footer',
				'p'         => $footer_id,
			));

			if ($cholot_footer->have_posts()) : while ($cholot_footer->have_posts()) : $cholot_footer->the_post();
					global $post; ?>

					<footer class="cholot-custom-footer clearfix">
						<?php the_content(); ?>
					</footer>

				<?php endwhile;
			endif;
			wp_reset_postdata();
		}
		//if page setting choose footer global
		else if (get_post_meta(get_the_ID(), 'cholot_footer_option', true) == 'global') {

			//if custom footer & list are selected in theme options
			if (get_theme_mod('custom_footer_setting_value') == 'custom' && get_theme_mod('cholot_select_footer') != '') {

				$footer_id =  get_theme_mod('cholot_select_footer');

				$cholot_footer = new WP_Query(array(
					'posts_per_page'   => 1,
					'post_type' =>  'footer',
					'p'         => $footer_id,
				));

				if ($cholot_footer->have_posts()) : while ($cholot_footer->have_posts()) : $cholot_footer->the_post();
						global $post; ?>

						<footer class="cholot-custom-footer clearfix">
							<?php the_content(); ?>
						</footer>

					<?php endwhile;
				endif;
				wp_reset_postdata();
			} else {
				get_template_part('loop/bottom', 'footer');
			}

			//if no footer
		} else if (get_post_meta(get_the_ID(), 'cholot_footer_option', true) == 'none') {
			//do nothing
		} else {

			//if else (standard footer)
			get_template_part('loop/bottom', 'footer');
		}

		//if not single page/post
	} else {
		//if custom footer & list are selected in theme options
		if (get_theme_mod('custom_footer_setting_value') == 'custom' && get_theme_mod('cholot_select_footer') != '') {

			$footer_id =  get_theme_mod('cholot_select_footer');

			$cholot_footer = new WP_Query(array(
				'posts_per_page'   => 1,
				'post_type' =>  'footer',
				'p'         => $footer_id,
			));

			if ($cholot_footer->have_posts()) : while ($cholot_footer->have_posts()) : $cholot_footer->the_post();
					global $post; ?>

					<footer class="cholot-custom-footer clearfix">
						<?php the_content(); ?>
					</footer>

				<?php endwhile;
			endif;
			wp_reset_postdata();
		} else { //standard footer
			get_template_part('loop/bottom', 'footer');
		}
	}
} ?>