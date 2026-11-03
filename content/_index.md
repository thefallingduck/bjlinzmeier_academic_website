---
title: ''
summary: Ben Linzmeier studies fossil and modern shells at the University of South Alabama. Learn about paleontology research and how to study geology in Mobile, Alabama.
seo:
  title: 'Ben Linzmeier: Paleontology & Geology at South Alabama'
date: '2026-10-27'
type: landing
sections:
- block: gallery
  id: gallery
  content:
    title: ''
    items:
    - src: media/SIMS-pit.jpg
      caption: A SIMS pit
    - src: media/Morocco-outcrop.jpg
      caption: Morocco
    - src: media/Ammonite-gold.jpg
      caption: Ammonite
    - src: media/ROM_Nautilus.jpg
      caption: Nautilus
  design:
    layout: slideshow
    aspect_ratio: wide
    autoplay: true
    autoplay_interval: 5000
    caption_position: overlay
    lightbox: false
    css_class: 'max-w-3xl mx-auto'
- block: resume-biography-3
  content:
    username: me
    text: ''
    button:
      text: Download CV
      url: cv.pdf
    headings:
      about: Biography
      education: Education
      interests: Interests
  design:
    background:
      gradient_mesh:
        enable: true
    name:
      size: md
    avatar:
      size: medium
      shape: circle
- block: cta-card
  content:
    title: Interested in paleontology or geology?
    text: |-
      I mentor undergraduates in paleontology research at the University of South Alabama. Whether you are in high school, at a community college, or already here, I can help you find a way to start.
    button:
      text: Study paleontology and geology at South Alabama
      url: study-paleontology/
  design:
    card:
      css_class: bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-600 text-white shadow-2xl
      css_style: ''
- block: collection
  id: papers
  content:
    title: Featured Publications
    filters:
      folders:
      - publications
      featured_only: true
  design:
    view: article-grid
    columns: 2
- block: collection
  content:
    title: Recent Publications
    text: ''
    filters:
      folders:
      - publications
      exclude_featured: false
      exclude_publication_type: conference-abstract
  design:
    view: citation
- block: collection
  id: talks
  content:
    title: Recent & Upcoming Talks
    filters:
      folders:
      - events
  design:
    view: card
- block: collection
  id: posts
  content:
    title: Recent Posts
    page_type: blog
    count: 5
    order: desc
    filters:
      folders:
      - blog
  design:
    view: card
- block: collection
  id: projects
  content:
    title: Projects
    filters:
      folders:
      - projects
  design:
    view: article-grid
    columns: 3
    show_date: false
    show_read_time: false
- block: contact-info
  id: contact
  content:
    title: Contact
    subtitle: ''
    visit_title: Visit
    connect_title: Connect
    address:
      lines:
      - Department of Earth Sciences
      - Earth and Life Sciences Building (ELSB), Room 343
      - 5871 USA North Drive
      - Mobile, AL 36688
    office_hours:
    - 'Monday, Wednesday, Friday: 9:00 to 11:00 AM'
    - 'Tuesday, Thursday: 9:00 to 9:30 AM'
    email: blinzmeier@southalabama.edu
    phone: (251) 460-7575
    prospective:
      title: Book an appointment
      text: Schedule time to meet during office hours.
      button:
        text: Open calendar
        url: https://calendly.com/bjlinzmeier
    map_url: https://www.southalabama.edu/campusmap
    show_form: true
    form_action: /contact-thanks/
---

