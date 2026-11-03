---
title: Courses
summary: 'I teach the following courses:'
type: landing
# HIDDEN: nothing under /courses/ is published. To bring courses back, delete this `build:` block
# and the first cascade entry below, and re-add the Courses link in config/_default/menus.yaml.
build:
  render: never
  list: never
cascade:
- build:
    render: never
    list: never
- target:
    path: '{/courses/*/**}'
  type: docs
  params:
    show_breadcrumb: true
sections:
- block: collection
  id: courses
  content:
    title: Courses
    filters:
      folders:
      - courses
      kinds:
      - section
    text: 'I teach the following courses:'
  design:
    view: article-grid
    show_read_time: false
    show_date: false
    show_read_more: false
    columns: 1
---

