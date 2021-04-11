---
widget: slider
headless: true  # This file represents a page section.

# ... Put Your Section Options Here (section position etc.) ...
weight: 10

# Slide interval.
# Use `false` to disable animation or enter a time in ms, e.g. `5000` (5s).
interval: 10000

# Minimum slide height.
# Specify a height to ensure a consistent height for each slide.
height: 400px

item:
  - title: A SIMS pit
    #content: 'A SIMS pit'
    # Choose `center`, `left`, or `right` alignment.
    align: right
    # Overlay a color or image (optional).
    #   Deactivate an option by commenting out the line, prefixing it with `#`.
    overlay_color: '#666'  # An HTML color value.
    overlay_img: SIMS-pit.jpg  # Image path relative to your `assets/media/` folder
    #overlay_filter: 0  # Darken the image. Value in range 0-1.
    # Call to action button (optional).
    #   Activate the button by specifying a URL and button label below.
    #   Deactivate by commenting out parameters, prefixing lines with `#`.
    #cta_label: Download my app
    #cta_url: 'https://example.org'
    #cta_icon_pack: fas
    #cta_icon: graduation-cap
  - title: Morocco
    align: left
    overlay_img: Morocco-outcrop.jpg
  - title: Ammonite
    #content: 'I am left aligned 😄'
    align: left
    #overlay_color: '#555'
    overlay_img: Ammonite-gold.jpg
    #overlay_filter: 0.5
  - title: Right
    #content: 'I am right aligned 😄'
    align: left
    font_color: '#555'
    #overlay_color: '#333'
    overlay_img: ROM_Nautilus.jpg
    #overlay_filter: 0.5
---