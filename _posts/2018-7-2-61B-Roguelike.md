---
layout: post
img: /images/rogue/roguelike.gif
title: 61B Roguelike Game
---

While the previous class related post was on the first project of CS61A, this is skipping straight to the second project of CS61B. There were 4 or 5 projects in between the two, but my main problem with them was that for the most part they were nothing more than fancy fill in the blank exercises. This project changed up that format by giving a ton of freedom to the students in terms of implementation.

*Disclaimer: This won't really go into as much technical detail as other posts, since I'm obligated not to share too much information on how I implemented stuff for the sake of academic integrity.*

The objective of the project was to create a *roguelike* game. According to Wikipedia, a roguelike is defined by "procedurally generated levels, turn-based gameplay, tile-based graphics, and permanent death of the player character." In previous projects, we were usually handed a skeleton outline of the what we had to do, along with a predefined specification for how everything should be implemented. I had major qualms with this style of assignment, mainly because it locked you in to a single approach to problem solving, and often times the method headers gave away the tricks to the problem. But it was more or a less a necessary evil: there were 700+ students, and the autograder had to work with a predefined functions and classes to test.

That's why Project 2 was so exciting! The only rigid requirements we had were to use the graphics library that was provided. As for the more abstract goals, we were asked to:
1. Implement a player character with some form of movement
2. Randomly generated rooms and hallways
3. The ability to interact with the environment
4. A condition to win the game.

Since this isn't going to be a technical post anyway, I guess I'll go a bit into my background in video games. The two big influencers for my game were *Pokemon Mystery Dungeon*, and *Realm of the Mad God (RotMG)*, both 2D dungeon crawling games with roguelike aspects. Two of my favorite parts of the dungeons featured in RotMG is that while the game tells you exactly *where* you should be headed, the labyrinth-like dungeon only provides one path to get there -- everything else is just a dead end. When I was thinking up how I might implement this, I was struck by inspiration, which ended up going not being valid, and then by a Discrete Math exam. During some last minute review for that exam, I realized that the dungeons in RotMG were actually just an implementation of my third favorite type of graph: the tree. *(My first favorite is the n-dimensional hypercube graph, followed shortly by directed acyclic)*

![](/images/rogue/rotmg_abyss.png)

An example layout for *The Abyss of Demons*, a dungeon that I spent too much time grinding in in RotMG.

The strategy to make the dungeon was to generate a bunch of rooms, and the connect them with hallways until they formed a tree. If that sounds vague, its because it is. I really wish I could go into more detail here, but I can't. I will say that the trick to forming the tree was to make sure each room wasn't already connected to another before joining them. This is because if we treat each room as a node in a graph, then connecting two previously connected nodes would form a cycle, ruining the tree property of the graph. To check for connectedness, I ended up "inventing" a special class to keep track of what was already linked, only to be find out later in lecture that it was called a Disjoint Set and that it had already been figured out long before I came around :(

Anyway, the last step was to come up with a theme for the game. I thought it would be funny to name the game after Dwinelle Hall, a building on campus rumored to have been designed by two disagreeable architects. For a gameplay video, check out [my extra credit video](https://www.youtube.com/watch?v=HFTrWrPsLMQ), or don't! Anyway, that's all for this post. Sorry about the lack of code.

![](/images/rogue/dwinelle.jpg)

*Depiction of Dwinelle Hall, courtesy of the Daily Kale.*
