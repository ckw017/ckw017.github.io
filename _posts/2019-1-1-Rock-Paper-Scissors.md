---
layout: post
img: https://i.imgur.com/qegKRGV.png?1
title: Rock, Paper, Scissors, Fire, Water, Grass
tags: [Python, Data Collection, Game]
---
For those unfamiliar with the finer details of competitive Pokemon, it's basically just a fancy version of rock, paper, scissors. While RPS gives each player 3 options, a turn in pokemon consists of around 4-9 possibilities for each player. Each player then reveals his or her choice simultaneously, and the results of their actions play out. This makes it different than games like Tic Tac Toe, Chess, or Go where only one player is "in control" at a time, and instead more like a game of Poker where two players are forced to reveal their hands at the same time.

If you've heard of Pokemon, you probably know that the game has a type system ([no, not that kind](https://en.wikipedia.org/wiki/Type_system)). For example, the franchise mascot Pikachu is an electric type, while the fan favorite Charizard is a combination of flying and fire type. Different attacks are also assigned types. As you might expect, a water type move does extra damage (super effective) when used against a fire type opponent, while an electric type moves do no damage to ground types. In this sense, the game really is just an elaborate version of rock, paper, scissors, but with 18 different objects (weapons? implements? tchotchkes?) instead of three.

## Monotype

A normal battle can take place between any combination of the 600+ Pokemon allowed in competitive matches, with each player being allowed to choose up to six. The types of battles I was interested are placed under a constraint known as "Monotype," which is to say that all Pokemon must share a type. For example, a team consisting of Pikachu (electric), Voltorb (electric), and Magneton (electric/steel) is allowed, since all members are electric type (such a team is called "mono electric"). Conversely, a team consisting of Squirtle (water) and Charmander (fire) is disallowed.

 ![Pikachu](http://play.pokemonshowdown.com/sprites/xyani/pikachu-original.gif)
 ![Voltorb](http://play.pokemonshowdown.com/sprites/xyani/voltorb.gif)
 ![Magneton](http://play.pokemonshowdown.com/sprites/xyani/magneton.gif)

 *Pikachu, Voltorb, and Magneton form a valid "Mono Electric" team*

As you can imagine, competitive matches in this format can be quite one-sided for certain "matchups" (combination of types against each other). For example, the matchup of Mono Water vs. Mono Fire heavily favors the player using water, but it isn't as black as white as a game of rock, paper, scissors. Every so often, a fire teams do overcome water teams through a combination of luck and strategy. For example, some Mono Fire teams run the Pokemon Volcanion, which regains health when hit by water type attacks and knows the move *Solar Beam*, which does heavy damage to water types. We would expect fire teams using this Pokemon to perform better on average than those without it.

 ![Volcanion](http://play.pokemonshowdown.com/sprites/xyani/volcanion.gif)

 *Volcanion: a Fire/Water type, that is immune to water attacks*

This is just one particular case for one particular matchup of a potential 172. As you can imagine, there are all sorts of factors that actually contribute to how likely one type is likely to beat another, ranging anywhere from team composition, to special abilities, to esoteric game mechanics. Attempting to quantify this is where the fun part begins.

## Collecting Data
To start off, I decided to collect data from the popular online Pokemon simulator, [Pokemon Showdown](https://pokemonshowdown.com/). Showdown typically has \~10,000 users online during the day and upwards of \~1000 battles taking place at any given moment. During the time I spent collecting data, I found that roughly 12,000 monotype battle took place on a daily basis.

To collect data, I had to create a bot that hooked into Showdown's websocket interface and listened in onto all public battles. Chat bots that interact with the website's chat rooms already existed, however were heavily specialized for chat based interactions and were exclusively written for Node.js. I decided to write my own client in Python, which ended up being great practice with Python 3's async features and Object Relational Managers (all of the data is currently being stored in a PostgreSQL backend.).

There was a long, complicated, and at times frustrating step between collecting the raw data and getting out useful information. For the sake of brevity and sanity, this has been omitted.

## Results!
After collecting all and parsing all the data, we finally get to the my personal favorite part of this kind of process: staring at tables and hoping that it makes. Said tables can be found [here](https://docs.google.com/spreadsheets/d/1BU5OC5Q9Xw5zcgSzIfnbDw8X4AaiKbSN1L1jfyx7llc/edit?usp=sharing). The data has been split into the following groups: 1100-1300, 1300-1500, and 1500+. These refer to a matches [Elo rating](https://en.wikipedia.org/wiki/Elo_rating_system), which is a metric originally invented as a chess rating system that quantifies the skill of given players in the match. The minimum possible Elo is 1000, and the highest (for my purposes) is roughly 2000. I excluded matches rated between 1000 to 1100 because these tend to contain sketchy results as the result of player's things or hooligans writing bots that serve no purpose but to forfeit every match (this may be expanded on at a later time). Anyway, we can now look over some of the results. These are the 5 most one-sided matchups in the 1100-1300 range:

| matchup            |   |win_rate      |
|--------------------|---|--------------|
| fire vs. grass     |   | 0.8295302013 |
| steel vs. ice      |   | 0.8210023866 |
| fighting vs. dark  |   | 0.7970244421 |
| steel vs. fairy    |   | 0.7966850829 |
| fairy vs. fighting |   | 0.7950310559 |

*The win_rate refers to the probability that a wins in the matchup a vs. b*

As any Californian will tell you, the matchup of fire vs. grass heavily favors fire. The difference is now we know exactly how much it favors grass, and that it is in fact the worst matchup in the game for players of the 1100-1300 skill range. It is interesting to note that this matchup gets even worse with higher skill players, moving from ~83% to ~87% in the 1500+ range (this is however based on a far smaller sample size).

One of the first "unintuitive" matchups comes with bug vs. ice, with bug winning at around 71% of the time. Bug and Ice are as neutral of a matchup you can get. Bug attacks do neutral damage on ice types, and ice attacks do neutral types on bug types. So what's giving Bug its edge? Scizors. As in the Pokemon, Scizor. Scizor is Bug/Steel type with access to the steel type Bullet Punch, which always hits first. Thanks to Scizor's special ability, Bullet Punch also does 1.5 times more damage than usual. Scizor also gets a Mega-Evolution, which in essence means it gets punch even harder. Oh, and its super effective against ice types. Oof.

![Scizor](http://play.pokemonshowdown.com/sprites/xyani/scizor.gif)
![Scizor-Mega](http://play.pokemonshowdown.com/sprites/xyani/scizor-mega.gif)

*Scizor and Mega Scizor: a Steel/Bug Pokemon that can single-clawedly beat ice teams*

# Conclusion
Pokemon really is just a fancy version of rock, paper, Scizors.