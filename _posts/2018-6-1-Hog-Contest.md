---
layout: post
img: https://i.imgur.com/utz2X8V.gif
title: Hog Contest (Part 1)
tags: Python Berkeley Visualization 2018
---

The first project of my first CS class at Berkeley was to write the logic for a modified version of the dice game
[Hog](http://inst.eecs.berkeley.edu/~cs61a/fa17/proj/hog/). The game itself is pretty simple (roll die to score points, first to 100 wins),
and the project was more a less just a warm-up to get everyone used to Python syntax and higher order functions. The extra credit option,
however, was a bit more interesting.


![](/images/hog-gui.jpg)


The extra credit option was to create a "strategy" to compete against other students' submissions. In this context,
a strategy is a function that takes the current score, and outputs a number of die to roll. A basic strategy might
look something like 'lambda my_score, opp_score: 4', which would always roll 4. The suggested ideas included taking
advantages of some of the game mechanics, such as "Swine Swap," which switches the players' scores if one is an integer
multiple of another, and "Free Bacon," which let you get a set amount of points by choosing to roll zero die. This
sort of thing could be implemented through a whole lot of if-statements, but it begged the question: was there a more
precise way to make a strategy?

[![](/images/iteration0.jpg){:width="320px"}](/images/iteration0.jpg)


*A handmade strategy*

The answer was of course, yes! The process goes something like this: given a score state and "seed" opponent strategy, we want to know the optimal
number of dice to roll to maximize our odds of winning. How can we determine that? By adding up the probability of winning
in future score states. This is a recursive problem, with the base case being situations where a player is guaranteed to win
on that turn, for example, if someone has 99 points. Paired with memoization, you could calculate the optimal strategy fairly
quickly. This approach had one limitation however: the strategy was only an optimal counter strategy against the input strategy, and not necessarily
all strategies.

[![](/images/iteration1.jpg){:width="320px"}](/images/iteration1.jpg)

*The optimal counter strategy against the handmade strategy*

The solution to this is actually pretty interesting. To get a truly optimal strategy, we can take the output from one iteration as
the seed for the next. An interesting trend emerges as we do this: the win rate of the counter strategy gradually went down, until
it reached 50%. Additionally, once it reached 50%, the output strategy would be equivalent to the input strategy!

<iframe width="600" height="371" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSHv20ef9STEktZIhsttsDrPg-5DBtHDcbIfyTbquh56xGqkVaOt5ZdGMhRZ5rx_AA16l3rpf198zzZ/pubchart?oid=1321489337&amp;format=interactive"></iframe>

The implication of this is interesting. Consider this: If the output strategy is the same is the input strategy, then the best counter to that strategy is itself. If we have a strategy that is optimal against itself, then it must beat all other strategies.
In other words, since the best counter strategy can only win 50% of the time, all other strategies must win less than 50% of the time. Which in the context of the contest means that this strategy was guaranteed to either win or tie against all other opponents1


So, anyone who discovered this optimal strategy would have tied for first, right? Well, for better and worse, the course staff had accounted
for this, which I will continue in [another post](/Hog-Contest-2/). For now, here's some neat graphics of the strategies "evolving" and converging towards
the optimal strategy.

[![](/images/human_base.gif){:width="320px"}](/images/human_base.gif)
[![](/images/always_4_base.gif){:width="320px"}](/images/always_4_base.gif)


*Seeded with the handmade strategy and "always 4" strategy respectively*
