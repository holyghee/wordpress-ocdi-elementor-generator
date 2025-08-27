				<!--SIDEBAR START-->
				<div class="col-md-4 sidebar">
				    <div class="sidebar-inner">
				        <?php if (function_exists('dynamic_sidebar')) {
							if (is_active_sidebar('default-sidebar')) {
								dynamic_sidebar('default-sidebar');
							}
						} ?>
				    </div>
				</div>
				<!--/.sidebar-->
				<!--SIDEBAR END-->