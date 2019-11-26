---
layout: post
img: /images/tiddlywiki/berry.png
title: Starting my own personal wiki
---

*"Think of the @TiddlyWiki as a markdown processor with a Turing-complete turbo-charged hyper-drive that becomes your external brain. Start intertwingling your ideas. Simple TWs use just markdown - but advanced TWs can do virtually anything."*

 -- [Joe Armstrong](https://twitter.com/joeerl/status/1083249244897796096?s=20), creator of erlang

Disclaimer: leading with this quote makes it feel like I'm trying to sell you on this tool as some kind of organizational panacea. I'm not. The introduction to this post is just really long so I needed a way to convince you to keep scrolling : )

Recently one of my friends had their backpack stolen along with their work laptop, phone, and wallet. While upset about the loss of their hardware and valuables it wasn't their main concern, since both sets of items were replaceable. What they were more concerned about were the photos on their phone and, to my surprise, their journal.

There's a large stretch of my life that's pretty much undocumented outside of my memories ranging from around 2003 to 2013. The first three years of my life are pretty fleshed out in my family's scrapbooks. And after 2013 most of my peers had gotten access to smartphones and social media, so some form of what I was up to exists out there. But between those two times not many photos of me were taken, or at least preserved, outside of group photos of extended families and middle school yearbooks. This didn't really bother me for most of my life. In fact, there's [a lot of concern today](https://well.blogs.nytimes.com/2016/03/08/dont-post-about-me-on-social-media-children-say/) about parents over-documenting their child's upbringing on social media when the kid is still too young to consent to the release of information that will be more or less impossible to retract from the clutches of indexers and dataminers unaffiliated with the original site. Imagine in 35 years when tabloids dig up videos of toddler tantrums as ammunition against the temperment of presidential candidates! 

On the other hand, personal documentation is largely beneficial. Being able to keep track of day-to-day events, how time was spent, and how you felt gives a lot of great information that you can use to get to know yourself and to keep track of beneficial or harmful patterns in your life. Moreover a scheduled recap at the end of every day is a nice memory exercise. Relying purely on memory works sometimes, but for me anything after a week tends to deteriorate rapidly. I've tried journaling in the past but to put it plainly I'm really bad at managing physical mediums: notebooks inevitably get repurposed and notepads blink out of existence. And even if I were worthy of handling real, non-digital, non-e-prefixed paper, scheduling in a time at the end of the day to just write things out is sort of out of place with my workflow for school which revolves around a lot of markdown files, repos, and other things from removed from the domain of dead trees.*

\* A [study](https://journals.sagepub.com/doi/abs/10.1177/154193120905302218?casa_token=3sRkvfe5L-EAAAAA%3AfvzReNSf5xZLCSf7yyA4_dhhRgAIej7ZpF86wJ6zhG_JwNVXnE1pjJIA97wRiXsBwYPSui6o_Q&) suggests that writing on dead trees is better for memory

Introducing TiddlyWiki: "a non-linear personal notebook." 
You can read all about it [here](https://tiddlywiki.com/), which is itself a TiddlyWiki that documents its own features. To summarize what it is to me:

* A journal that won't get crumpled in my bag and can embed images
* A flexible data store with search and tagging for text documents, PDFs, images, and generic file types
* A notetaking tool that doesn't require me to recompile LaTeX every time I forget a \end statement
* A more flexible Google Drive that I don't have to entrust the confidentiality of to a cloud service

Other people use it as a TODO list and task manager, but I don't quite see it as the best choice of tool for that.

Personal wiki's aren't a new idea whatsoever, dating back to the [Memex](https://en.wikipedia.org/wiki/Memex) in 1945. The Memex was imagined to be a device in the far future that could compress documents encoding a person's knowledge and indexing it for rapid retrieval, not a farfetched idea at all in hindsight! [MyLifeBits](https://en.wikipedia.org/wiki/MyLifeBits) is an ongoing project by [Gordon Bell](https://en.wikipedia.org/wiki/Gordon_Bell) inspired by Memex to document everything he's encountered. While my wiki and Bell's are personal for privacy reasons, people on [this list](https://github.com/RichardLitt/meta-knowledge) have entirely open ones, (hopefully) cleansed of any sensitive information.

So far I'm really enjoying the experience. Journals are easy to create, format, and update either throughout the day or as I recall details. Tag's allow hierachies to be formed, so at the end of each week I can link all the journal entries to a larger summary of the week, and as I approach the end of years and months the same techniques can be applied recursively.  Inline LaTeX means that I can actually take notes and the fact that it is a "wiki" means I can hyperlink together internal information.

One thing I'm excited to use is tagging a journal entry with "future" to mark it as something that I want to reflect on at a certain time. For example, right now most of my stress comes from a combination of summer job search and exam season. By the time these problems are resolved, I think it would be nice to have a one-for-one correspondence between present and future me. I found that by far my favorite writing assignment in high school was one of the first: to write a letter to myself at graduation, and then "write back" when the time came. I think both ends of the correspondence forced me to really consider my life holistically and in longer term than I'm ever forced to on a day-to-day basis. In particular, it was somewhat reassuring to see that all the worry's my freshman year incarnation had worked out in one way another.

As I mentioned, for now this is a purely personal wiki. I don't plan to make any of it public, though the version I use is hosted off a node server and displayed in browser. If I get good enough with the tools I might just fork off the notetaking and course related stuff to a separate public entity for the pedagogical greater good. Moreover, I can see this becoming a nice place to prototype ideas for more blog posts. As you may notice, there's a very apparent gap in content here! Part of the reason I've been hesitant to publish anything is because there's a lot of careful checking that I do before I put anything out, and these formalisms make me reluctant to start at all. Being able to just write out ideas lazily (no full sentences, grammar structure, special formats) let's me get started easily, and starting tends to be half the battle for writing.

Because I'm bad at conclusions, enjoy some snippets of how I'm currently using my personal wiki! And thanks for reading.

![](/images/tiddlywiki/fstring.png)

*Notetaking on a particularly interesting python library, as well as a hint towards a future post : )*

![](/images/tiddlywiki/journal.png)

*Journal entry aggregation and some nice $\LaTeX$ rendering*

![](/images/tiddlywiki/lecture.png)

*I'm almost good enough to keep with lectures that don't have heavy notation*

![](/images/tiddlywiki/fullview.png)

*Images (shoutout to the Berkeley Alum artist Yuumeii) can be uploaded and tagged. Side bar on the side has search, recently used, and other tools (which can be extended programmatically from within the wiki!)*