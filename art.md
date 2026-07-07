---
layout: page
title: Plotter Art
permalink: /art/
---

*Last updated: July 5th, 2026*

---

<div class="posts">
<div class="post">
This is primarily art I've drawn with my pen plotter.
Everything here is drawn with an AxiDraw v3, usually with either a Sakura Gelly
Roll pen (white) or a Pentel 0.05 Pointliner (black).
<br><br>
As of 2026, I've also animated some plotter pieces on an
<a href="https://github.com/xanderchinxyz/OpenGhost" target="_blank">OpenGhost</a> display.

</div>
{% for plot in site.plots reversed %}
<article class="post">
    <div class="flex-container" style="flex-wrap: wrap">
        {% if plot.video %}
        <video src="{{ site.baseurl }}{{ plot.img }}" style="outline:none;max-width:min(300px, 100%);" autoplay loop muted playsinline controls="controls"></video>
        {% else %}
        <a href="{{ site.baseurl }}{{ plot.img }}" style="display:contents">
        <img src="{{ site.baseurl }}{{ plot.img }}" style="max-width:min(300px, 100%);">
        </a>
        {% endif %}
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
