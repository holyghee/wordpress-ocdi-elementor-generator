# DAA Pattern Analysis Report
Generated: 2025-08-28 02:08:50

## Executive Summary

Analyzed **7 templates** containing **168 widget instances** across **18 unique widget types**.

## Key Findings

### 1. Most Used Widgets
- **text-editor**: 37 instances
- **cholot-title**: 22 instances
- **divider**: 22 instances
- **image**: 19 instances
- **cholot-texticon**: 18 instances


### 2. Golden Patterns Identified

Found **18 golden patterns** representing the most common parameter combinations for widgets.

### 3. Widget Hierarchy

Top-level containers that can nest other widgets:


### 4. Responsive Design Patterns

Identified **18 widgets** with responsive breakpoint parameters.

### 5. Content Injection Zones

Key areas for dynamic content:
- **rdn-slider**: 16 text fields
- **cholot-texticon**: 10 text fields
- **video**: 1 text fields
- **text-editor**: 2 text fields
- **cholot-title**: 6 text fields


## Validation Results

## Recommendations for Generator

### Priority Implementation Order
1. text-editor
2. cholot-title
3. divider
4. image
5. cholot-texticon
6. icon
7. cholot-text-line
8. cholot-team
9. cholot-contact
10. cholot-button-text


### Critical Parameters by Widget

**rdn-slider**:
  - slider_list
  - align
  - title_typo_typography
  - title_typo_font_size
  - title_typo_font_weight
**image**:
  - image
**cholot-texticon**:
  - icon
  - title_text_margin
  - title
  - title_typography_typography
  - title_typography_font_size
**video**:
  - youtube_url
  - vimeo_url
  - dailymotion_url
  - show_image_overlay
  - image_overlay
**text-editor**:
  - editor
  - typography_typography
  - _margin
  - typography_font_weight
**cholot-title**:
  - title
  - desc_typography_typography
  - desc_typography_font_size
  - desc_typography_font_weight
  - desc_typography_line_height
**divider**:
  - weight
  - color
  - width
  - align
  - gap
**cholot-team**:
  - title
  - text
  - image
  - team_height
  - team_icon
**cholot-testimonial-two**:
  - show_desktop
  - testi_list
  - title_typography_typography
  - title_typography_font_size
  - title_typography_font_size_mobile
**icon**:
  - selected_icon
  - view
  - primary_color
  - secondary_color
  - size


## Pattern Groups

### Always Together Parameters

**rdn-slider**: align, arrow_bg_color, arrow_bg_color_hover, arrow_color, arrow_color_hover

**image**: _margin, background_hover_transition, css_filters_hover_brightness, css_filters_hover_css_filter, image

**cholot-texticon**: __fa4_migrated, _border_border, _border_color, _border_width, _padding

**video**: dailymotion_url, image_overlay, lightbox, lightbox_content_animation, play_icon_color

**text-editor**: _margin, align, editor, text_color, typography_font_size

**cholot-title**: _margin, _z_index, align, desc_typography_font_family, desc_typography_font_size

**divider**: align, color, gap, weight, width

**cholot-team**: _margin, background_background, background_bg_width, background_color, background_position

**cholot-testimonial-two**: _margin, content-align, icon_fsize, icon_lheight, icon_size

**icon**: _margin, _z_index, align, border_width, icon_padding

**cholot-text-line**: _background_background, _background_bg_width, _background_color, _background_image, _background_position

**cholot-contact**: btn_bg, btn_bg_hover, btn_border, btn_border_color, btn_border_radius

**cholot-button-text**: _margin, align, btn_color, btn_color_hover, btn_sub

**icon-list**: divider_color, icon_align_tablet, icon_color, icon_list, icon_size

**google_maps**: address, css_filters_css_filter, css_filters_hover_css_filter, css_filters_saturate, height

**cholot-post-four**: blog_column, blog_post, box_shadow_box_shadow, btn_bg_hover, btn_border_border

**cholot-sidebar**: title_typography_font_size, width

**cholot-gallery**: caption_show, gallery, gallery_height, gallery_height_mobile, gallery_margin
