---
layout: page
title: Plotter Art
permalink: /art/
---

*Last updated: August 20th, 2020*

---

<div class="posts">
<div class="post">
<b>Under construction</b>: This is where I'll be dumping art drawn with my pen plotter!
Everything here is drawn with an AxiDraw v3, usually with either a Sakura Gelly
Roll pen (white) or a Pentel 0.05 Pointliner (black).
</div>
{% for plot in site.plots reversed %}
<article class="post">
    <div class="flex-container" style="flex-wrap: wrap">
        <a href="{{ site.baseurl }}{{ plot.img }}">
        <img src="{{ site.baseurl }}{{ plot.img }}" style="max-width:300px;">
        </a>
        <div class="text-preview" style="width: 60%">
        <h1><a href="{{ site.baseurl }}{{ plot.img }}">{{ plot.title }}</a></h1>
        <i>{{plot.date | date: "%B %Y" }}</i>
            <div class="entry">
                {{ plot.content }}
            </div>
        </div>
    </div>
</article>
{% endfor %}
</div>