#! /usr/bin/python

import os

for fname in os.listdir('./_tagarchive'):
    os.remove(os.path.join('./_tagarchive', fname))

with open('_site/tags.txt', 'rt') as f:
    tags = set(f.read().splitlines())

template = \
"""
---
layout: tagarchive
value: {}
permalink: /tag/{}
---
""".strip()

for tag in tags:
    if not tag:
        continue
    title = tag.lower().replace(' ', '-')
    path = './_tagarchive/{}.md'.format(title)
    with open(path, 'wt') as f:
        f.write(template.format(tag, title))
