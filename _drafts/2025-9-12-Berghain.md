---
layout: post
img: /images/berghain/thumbnail.jpg
title: Berghain bouncer challenge
excerpt_separator: <!--more-->
---

I fell down a bit of a rabbit hole the other day after seeing [a post on r/sanfrancisco](https://www.reddit.com/r/sanfrancisco/comments/1n6nx67/at_this_point_it_feels_like_these_tech_startups/)
about a cryptic billboard in Nob Hill:

<!--more-->
<img src="/images/berghain/billboard.jpg" style="max-height: 40vh"><br>

You can check the thread for the decoding method, but once solved it reveals a link to
[a challenge](https://listenlabs.ai/puzzle) which I'll be discussing my solution for.
The gist of the challenge is to develop strategies for a souped up version of
[the secretary problem](https://en.wikipedia.org/wiki/Secretary_problem):

> You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people
> while satisfying constraints like "at least 40% Berlin locals", or "at least 80%
> wearing all black". People arrive one by one, and you must immediately decide whether
> to let them in or turn them away. Your challenge is to fill the venue with as few
> rejections as possible while meeting all minimum requirements.

The challenge involves three different scenarios, each with different attributes and requirements.

## Scenario 1

Scenario 1 is the simplest scenario with only two different constraints:
* At least 600 young people.
* At least 600 well-dressed people.

The following statistics are also provided:
* 32.25% of the time guests are young.
* 32.25% of the time guests are well-dressed.
* Being young and being well-dressed have a correlation coefficient of ≈0.183. In other
  words, ≈14.4% of the time guests are both well-dressed and young.
* You can assume each guest is sampled i.i.d. from this distribution.

You can take a moment to think about how you would solve this problem. If
you were as generous as possible and allow the first 1000 people you see in, you would
end up on average with 322 young people and 322 well-dressed people -- well below the
minimum requirement of 600 in both categories. In other words, you're going to need to
be selective. However, being too selective will increase the number of people you reject
before filling the venue and make your score worse.

One detail which stood out to me was given a capacity of 1000, there
must be an overlap of at least 200 between the 600 young people and 600
well-dressed people once the venue is filled, i.e. an implicit requirement:
* At least 200 people who are both young and well-dressed.

Notice also if we're not careful with who we reject, we might end up in an unwinnable state.
Say we're in this state:
* We've let in 200 guests that are young and well-dressed.
* We've let in 401 guests that are young, but not well-dressed.
* We have 399 spaces left in the venue.
* We still need 400 well-dressed guests, which is no longer feasible.

In this case, we let in too many guests that are only young and didn't leave enough space
for 600 well-dressed guests. We can capture these constraints by defining a few variables:
* `space`: The remaining space in the venue. This starts at 1000 and decrements every time we accept someone until it hits 0.
* `need_y`: The number of young people we still need. This starts at 600 and decrements every time we accept a young person until it hits 0.
* `need_w`: The number of well-dressed people we still need. This starts at 600 and decrements every time we accept a well-dressed person until it hits 0.

We can derive a few more values from these:
* `need_wy = max(0, need_y + need_w - space)`: The number people who are both young and well-dressed that we still need.
* `slack_y = need_y - need_wy`: The number of guests that are young but not well-dressed that we can safely accept to meet requirements.
* `slack_w = need_w - need_wy`: The number of guests that are well-dressed but not young that we can safely accept to meet requirements.

Using the slack variables, we can determine if it's safe to allow in guests that are only
young or only well-dressed. For example, consider the state where `space=100`, `need_y=50`, and `need_w=100`:
* `need_wy = max(0, 50 + 100 - 100) = 50`: We need at least 50 guests that are both young and well-dressed.
* `slack_y = 50 - 50 = 0`: We do not have space to let in any guests that are young but not well-dressed.
* `slack_w = 100 - 50 = 50`: We can safely let in 50 guests that are well-dressed but not young.

Encoding this into a function:

```python
def accept(person: Dict[str, bool]) -> bool:
  if person["young"] and person["well_dressed"]:
    # No downside to accepting someone who
    # meets every requirement.
    return True
  if person["young"] and slack_y > 0:
    return True
  if person["well_dressed"] and slack_w > 0:
    return True
  if need_w + need_y < space:
    # We've fulfilled enough of the requirements
    # that we can afford to let in an arbitrary
    # person here.
    return True
  return False
```

Using this strategy we can fill the venue and meet the requirements with an average of ≈892 rejections.

# Scenario 2

<style>
table{
    border-spacing: 50px;
    border:1px solid #000000;
}

th {
    border: 1px solid #000000;
    padding: 0px 10px 0px 10px;
    max-width: 40vw;
}

td{
    border:1px solid #000000;
    padding: 0px 10px 0px 10px;
    max-width: 40vw;
}
</style>

Scenario 2 removes the young and well-dressed constraints and introduces four new ones:
* At least 750 Berlin locals.
* At least 650 techno loving people.
* At least 450 well-connected people.
* At least 300 creative people.

We also receive the following information about the distribution people are sampled from:
* 39.8% of the time guests are Berlin locals.
* 62.65% of the time guests are techno lovers.
* 47% of the time guests are well-connected.
* 6.227% of the time guests are creative.
* Well-connected and Berlin local have a correlation coefficient of ≈0.5724.
* There are correlation coefficients for all the other possible pairings of attributes,
which I'm omitting for brevity.

At first it appears the number of constraints has doubled, however in practice we don't
really need to worry about the minimum of 450 well-connected people. Since the correlation
with Berlin locals is high and the minimum for Berlin locals is 750, we end up satisfying
the well-connected minimum the vast majority of the time just by trying to meet the Berlin
locals minimum. This narrows down the problem to Berlin locals (`b`), techno lovers (`t`) and
creative people (`c`). Reusing the ideas from Scenario 1, my first attempt looked like this:

```python
def accept(person: Dict[str, bool]) -> bool:
  if person["berlin_local"] and person["techno_lover"] and person["creative"]:
    # No downside to accepting someone who
    # meets every requirement.
    return True
  if person["creative"] and need_c > 0:
    # Creatives are rare, accept all of the ones we encounter
    # if we need them.
    return True

  need_bt = max(0, need_b + need_t - space)
  # We include `need_c` in the slack calculations here
  # so we have space to take every creative person we see.
  slack_b = need_b - need_bt - need_c
  slack_t = need_t - need_bt - need_c

  if person["berlin_local"] and person["techno_lover"] and need_bt > 0:
    return True
  if person["berlin_local"] and slack_b > 0:
    return True
  if person["techno_lover"] and slack_t > 0:
    return True
  if need_b + need_t + need_c < space:
    # We've fulfilled enough of the requirements
    # that we can afford to let in an arbitrary
    # person here.
    return True
  return False
```

This works okay, but isn't necessarily optimal due to interactions between the three
constraints that require us to make tradeoffs. For example, accepting too many people
who are creative but don't contribute to other constraints increases the required number of people
who must be both Berlin local and techno lovers, which in some cases can become the bottleneck.
While we could try to hand pick some heuristics to balance these tradeoffs, what if instead we
programmatically found a set of acceptance/rejection rules?

We can do this using [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming).
Our goal is to find a function:

`policy(space, need_b, need_t, need_c) -> {acceptable}`

where `acceptable` is a set containing the types of people we should accept. Note that
there are eight mutually exclusive types of people who we might encounter depending on different possible
combinations of attributes:

<!--
const PROBABILITIES: [f32; 8] = [
    0.06611124895048826,   // 000
    0.0036587510495119033, // 001
    0.5154897510495119,  // 010
    0.016740248950488097, // 011
    0.295192751049512,  // 100
    0.008537248950488102, // 101
    0.06093624895048804,  // 110
    0.033333751049511896, // 111
];
-->

| **Shorthand**   | **Percentage** | **Description** |
|:----------------|---------|--------------------------------------------|
| `N`             | 6.62%   | People with no relevant attributes. |
| `B`             | 29.52%  | People who are only Berlin local.   |
| `T`             | 51.55%  | People who are only techno lovers.  |
| `C`             | 0.37%   | People who are only creative.       |
| `BC`            | 0.85%   | People who are only Berlin local and creative.     |
| `BT`            | 6.09%   | People who are only Berlin local and techno lovers.      |
| `TC`            | 1.67%   | People who are only techno lovers and creative. |
| `BTC`           | 3.33%   | People who are Berlin local, techno lovers, and creative.       |

In order to optimize the policy function, we'll need a second function:

`cost(space, need_b, need_t, need_c) -> float`

This tells us the expected number of people we'll reject when going from a given state to the goal
state where the venue is filled and meets all constraints. As a base case, we know that:

`cost(0, 0, 0, 0) = 0`

This represents the state where we've already reached all our goals and no further work is needed. Let's
consider a non-trivial case of the cost function:

`cost(10, 9, 0, 1)`

In other words, we have 10 spaces left and still need 9 Berlin locals and
1 creative. Say we have a policy where we only accept people in the set `{B,C,BC}` from this state.
Using this policy, how many rejections would we expect to make before we see someone
that meets these criteria? Each person we encounter has a 29.52% + 0.37% + 0.85% = 30.74% chance
of meeting our acceptance criteria. Using the formula for [expected number of trials to first success](https://en.wikipedia.org/wiki/Geometric_distribution)
we expect to see an acceptable person after $$1/p = 1/0.3074 \approx 3.25$$ attempts. Since
we accept the person once we encounter them, we expect on average $$3.25 - 1 = 2.25$$
rejections.

Once we've found an acceptable person, we need to account for the expected number of rejections
we'll make after accepting that person. We can compute this by recursively calling into
the cost function. For simplicity, I'm making up values for the recursive calls:
* There's a 29.52/30.74 = 96.03% chance the person will be `B`. The expected cost after we accept `B` is:<br> `cost(9, 8, 0, 1) = 30`.
* There's a 0.37/30.74 = 1.20% chance the person will be `C`. The expected cost after we acccept `C` is:<br> `cost(9, 9, 0, 0) = 18`.
* There's a 0.85/30.74 = 2.77$ chance the person will be `BC`. The expected cost after we accept `BC` is:<br> `cost(9, 8, 0, 0) = 16`.

We can do a weighted sum of the values of the recursive cost calls by their probabilities, giving us:

```python
# Assuming we accept {B, C, BC}
cost_after_accepting = (0.9603 * 30) + (0.012 * 18) + (0.0277 * 16)
                     = 29.4682
```

Finally, we can combine this with the expected cost of finding an acceptable person from earlier, giving us:

```python
# Assuming we accept {B, C, BC}
total_cost = cost_of_finding + cost_after_accepting
           = 2.25 + 29.4682
           = 31.7182
```

These calculations assume we accept anyone in the set `{B,C,BC}` and reject everyone else.
To find the optimal policy, we can run the calculation for each of the 256 possible
acceptance strategies in `powerset({N,B,T,C,BT,BC,TC,BTC})`, and then choose the
policy with the lowest cost. Once we find the best cost and the associated
policy, we can use those values for all future calls to `cost(10,9,9,1)` and
`policy(10,9,0,1)`.

Now that we have a method for finding the optimal accept/reject policy at every possible
game state, we can recursively run this algorithm and generate a lookup table. Assuming
each policy is encoded as 1 byte, computing the full space of possible game states would
require roughly:

`1000 * 750 * 650 * 300 = 146_250_000_000 entries` (136.2 GiB)

For the competition, I ended up compromising and only computing a subset of the full
lookup table for use in the latter half of the game, i.e. up to:

`500 * 330 * 300 * 150 = 7_425_000_000 entries` (6.91 GiB)

In other words, we use the optimal strategy once we're roughly halfway done with
each of our constraints. How about for the beginning half of the game? I ended up using the
same dynamic programming approach, however slightly augmenting the policy function to only take three parameters:

`policy2(space, need_b + need_t, need_c) -> {acceptable}`

In this version, we combine the constraints for Berlin locals and techno lovers into a
single parameter in our policy and cost function. This allows us to drastically reduce
the size of the lookup table to:

`1000 * (750 + 650) * 300 = 420_000_000 entries` (400 MiB)

This reduction comes at a cost: the policy cannot distinguish
between the individual constraints for `need_b` and `need_t`. Despite this, it gives us
a good enough method to balance the tradeoffs between creative people and people
who are both Berlin local and techno lovers, which are the main
two bottlenecking constraints. Note we must be careful not to violate `slack_b` and `slack_t`
constraints while following `policy2`, since it doesn't have enough information to account for those
on its own. In pseudo-code, the two combined policies look like:

```python
def accept(person: Dict[str, bool]) -> bool:
    if capacity < 500 and need_b < 330 and need_t < 300 and need_c < 150:
        # All of our constraints have progressed enough that we can use
        # the full lookup table.
        return policy(capacity, need_b, need_t, need_c).allows(person)

    # Trust any rejections from policy2.
    if not policy2(capacity, need_b + need_t, need_c).allows(person):
        return False

    # Trust policy2 if it accepts C, BC, TC, BTC, or BT.
    if person["creative"] or (person["berlin_local"] and person["techno_lover"]):
        return True

    # At this point, the person can be one of {B, T, N}
    # We need to do extra filtering for B and T to avoid
    # winding up in unwinnable positions.
    need_bt = max(0, need_b + need_t - space)
    slack_b = need_b - need_bt - need_c
    slack_t = need_t - need_bt - need_c
    if person["berlin_local"]:
        return slack_b > 0
    if person["techno_lover"]:
        return slack_t > 0
    return False
```

This is the strategy I ended up using, which averages around 3820 rejections before fulfilling
all of the constraints.

# Scenario 3

Scenario 3 discards the previous 4 constraints, and introduces 6 new ones:
* At least 500 underground veterans.
* At least 650 international people.
* At least 550 fashion forward people.
* At least 250 queer friendly people.
* At least 200 vinyl collectors.
* At least 800 German speakers.

Luckily, just like last time most of these constraints tend to solve themselves. In
particular, only 3 constraints result in bottlenecks in practice: German speakers, international
people, and queer friendly people. Conveniently, this means we can plug the new
distribution and constraints into the dynamic programming method from Scenario 2 to
generate a new strategy. This averages around 4538 rejections before fulfilling all of the constraints.

# The Metagame

Now that we have our strategies, we can see how good they are compared to everyone else
on the leaderboard, right? Unfortunately, since the problem is inherently random there's
a bit of variance in everyone's submissions. To get a feel for this, the top of the
leaderboard on the day I joined the competition looked like this:

![](/images/berghain/leadersearly.jpg)

Let's take a closer look at the score of 716 in Scenario 1. Recall that for Scenario 1,
we need to fill the venue with 600 young people and 600 well-dressed people, each appearing
32.5% of the time. That means in order to get a score of 716, we need to see at least 600
young people among the first 1716 people we encounter (1000 accepts, 716 rejects). What
are the odds of this? We can model this as a [binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution)
with $$p=0.3225$$ and $$n=1716$$:

<img src="/images/berghain/binomialyoung.jpg" style="max-height:40vh"><br>*Shoutout to [stattrek.com](https://stattrek.com/online-calculator/binomial)!*

The probability that the first 1716 people will include at least 600 young people
is represented by the portion of the distribution to the right of the red dotted line,
which is approximately 0.9%. In other words, you need to submit your
strategy for Scenario 1 about 100 times before getting a sequence where it's even possible
to fulfill the young person requirement in 1716 people or less. We also have to take into account the well-dressed
requirement, which is also only possible 0.9% of the time (though it correlates with young people). Running simulations to find the
number of minimum number of people before they're both satisfiable, we get the following distribution:

<img src="/images/berghain/youngandwelldressed.jpg" style="max-height:40vh">

The part of the distribution below 1716 is almost impossible to see, but is cumulatively about 0.028%.
This means roughly 1 in 3531 attempts are solvable in 716 rejections or less.
If you want to win the contest, having a good strategy isn't enough -- you also need
to be lucky or to submit a lot.

Submitting a lot is a challenge in itself. To start, there is a rate limit of 10 submissions
every 15 minutes, i.e. 960 submissions per day. This on its own was reasonable, however
every 6 hours or so something in the sites networking stack seemingly blacklists traffic from
the IPs of everyone doing submissions. I'm not entirely sure if this is just a me problem, however from what I observed:
* The networking problem is tied to IPs, not accounts. For example, switching to a different WiFi
on the same account seemed to fix it. I assume if the organizers are actually trying to
ban me, they would just delete my account or email me about it.
* There is a page that shows active submissions where a consistent
group of 20 or so people are always resubmitting up to the rate limit. Whenever I
encounter the network problem, I also see progress on everyone else's submissions grind to halt.
* [This guy](https://news.ycombinator.com/item?id=45159393) on Hackernews also ran into it.

My workaround for this is to rent the cheapest tier of VM from [DigitalOcean](https://www.digitalocean.com/)
for a few cents per hour and run my submissions from there. Whenever it looks like the networking
issue is happening, a script tears down the old machine and spin up a new one with a new
IP. If this really wasn't just a me problem I'd be curious to hear what everyone else near
the top of the leaderboard was doing to circumvent this.

At the time of writing this I currently hold
first place. However, I don't expect it to last for very long since it's by a razor thin margin:

![](/images/berghain/areyouwinningson.jpg)

Normally it wouldn't make sense to publish a writeup on my strategy before the event is over,
but at this point I'm fairly confident that everyone in the running for first has comparable
strategies and the competition has turned into a lottery to see who can get the luckiest with their
submissions. I'll likely update this post again once the competition is over with some
additional commentary.

Anyway, if you found this interesting you might also like this writeup I did about a
similar competition back in 2022:
[Playing every game of Wordle simultaneously](/2025/08/24/Hyper-Wordle/). Thanks for reading!
