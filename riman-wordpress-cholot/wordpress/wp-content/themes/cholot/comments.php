<div class="comment-box 
<?php if (!have_comments()) {
    echo 'nocomm';
} ?>">
    <ul id=" comments" class="commentlist clearfix">
        <?php wp_list_comments('avatar_size=88&callback=cholot_comment'); ?>
    </ul>
</div>
<div class="pagination-comment clearfix"><?php paginate_comments_links(); ?> </div>
<?php comment_form(array('title_reply' => esc_html__('Leave a comment ', 'cholot'), 'comment_notes_before' => '', 'comment_notes_after' => '')); ?>