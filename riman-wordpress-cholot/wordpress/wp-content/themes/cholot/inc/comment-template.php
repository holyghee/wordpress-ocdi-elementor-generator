<?php function cholot_comment($comment, $args, $depth)
{

    extract($args, EXTR_SKIP);

    if ('div' == $args['style']) {
        $tag = 'div';
        $add_below = 'comment';
    } else {
        $tag = 'li';
        $add_below = 'div-comment';
    }
    ?>


<<?php echo esc_attr($tag) ?> <?php comment_class(empty($args['has_children']) ? '' : 'parent') ?>
    id="comment-<?php comment_ID() ?>">
    <?php if ('div' != $args['style']) : ?>
    <div id="div-comment-<?php comment_ID() ?>" class="comment-body clearfix">
        <?php endif; ?>
        <div class="comment-author vcard">
            <?php if ($args['avatar_size'] != 0) echo get_avatar($comment, $args['avatar_size']); ?>
        </div>

        <div class="comment-inner clearfix">

            <div class="comment-top clearfix">
                <div class="cm-name">
                    <p class="fn comment-author"> <?php comment_author_link(); ?></p>
                </div>
                <div class="comment-date"><i class="fa fa-clock-o"></i>
                    <?php
                        $d = "F jS Y";
                        $comment_date = get_comment_date($d);
                        echo esc_html($comment_date); ?>
                </div>

                <div class="reply">
                    <?php comment_reply_link(array_merge($args, array('add_below' => $add_below, 'depth' => $depth, 'max_depth' => $args['max_depth']))); ?><i
                        class="fa fa-long-arrow-right"></i>
                </div>
            </div>
            <div class="comment-text">
                <?php comment_text(); ?>
            </div>
            <div class="comment-bottom clearfix">
                <div class="comment-meta commentmetadata">
                    <?php edit_comment_link(); ?>
                </div>
                <?php if ($comment->comment_approved == '0') : ?>
                <em
                    class="comment-awaiting-moderation"><?php esc_html_e('Your comment is awaiting moderation.', 'cholot') ?></em>
                <br />
                <?php endif; ?>
            </div>
        </div>
        <?php if ('div' != $args['style']) : ?>
    </div>
    <?php endif; ?>
    <?php
    }