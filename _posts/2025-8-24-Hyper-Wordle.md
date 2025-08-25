---
layout: post
img: /images/wordle/wordle.jpg
title: Playing every game of Wordle simultaneously
excerpt_separator: <!--more-->
---

If you've fallen far enough down the [Wordle](https://www.nytimes.com/games/wordle/index.html) rabbit hole you may have heard of [Quordle](https://www.merriam-webster.com/games/quordle/#/),
a version of Wordle where you solve four words at once. If you're looking for more of a challenge,
Britannica has you covered with [Octordle](https://www.britannica.com/games/octordle/),
where you solve eight words at once. And of course any Wordler worth their salt should be able
to handle sixteen words, like in [Sedecordle](https://sedecordlegame.org).
And no, it doesn't [stop](https://duotrigordle.com/) [there](https://64ordle.au/):

<!--more-->

[![What hath God wrought?](/images/wordle/64-dle.jpg)](https://64ordle.au/)<br>
*Sexaginta-quattuordle isn't real, it can't hurt yo--*

One logical extreme of this trend would be to take the [list of 2315 valid secret words](https://scourway.com/wordle/zez8el/wordle-answers-list-2315-words-5-letters)
to create duomilia-trecenti-quindecordle, where each day the puzzle is a different permutation of those 2315[^1] words.
Despite how chaotic the user interface would need to be, this variant wouldn't be much of a challenge. Since
the same guess is applied to *all* 2315 words every turn, entering each of the 2315 secret words
in any order will always solve it with a perfect score of 2315 guesses.

But what if you could enter *different* guesses for each of the 2315 secrets each turn?
I call this Hyper Wordle since it can be viewed as an exponentially larger
version of normal Wordle:

<style>
table{
    border-spacing: 50px;
    border:1px solid #000000;
}

th{
    border: 1px solid #000000;
    padding: 3px;
    max-width: 40vw;
}

td{
    border:1px solid #000000;
    padding: 3px;
    max-width: 40vw;
}
</style>

| **Normal Wordle**                                                           | **Hyper Wordle**                                                                                          |
|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Secrets are chosen from the $$2315$$ possible 5-letter secret words.        | 2315 secrets are chosen from the $$2315!$$ possible permutations of 5-letter secret words.                 |
| Each turn a guess is chosen from $$12972$$ possible 5-letter words.[^2]         | Each turn 2315 guesses are chosen from $$12972^{2315}$$ possible tuples of 5-letter words. |
| Feedback is given in the form of $$5$$ colored squares.                         | Feedback is given in the form of $$5 \times 2315 = 11575$$ colored squares.                           |
| Your score is the number of 5-letter guesses needed to identify the secret. | Your score is the total number of 5-letter guesses needed to identify each word in the secret permutation.      |

Believe it or not, this is a real Wordle variant I ran into back in 2022 [as part of a competition](https://web.archive.org/web/20220521064114/https://botfights.ai/tournament/botfights_iv)
to see who could write the best Wordle solving program.
One way to play would be to treat each secret word in the permutation as its own game,
effectively playing 2315 independent games of Wordle. For example, if you used the optimal[^3] [Wordle strategy starting with the word `SALET`](https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle)
(average score of ≈3.4212 guesses) against every secret in the permutation,
submissions would always score exactly $$3.4212 \times 2315 = 7920$$
since every potential secret word always appears exactly once.

7920 is by no means a bad score, but can we do better? For example,
can we take advantage of the fact that the secrets are permuted *without replacement* to
gain extra information? After all, even if `SALET` is optimal for Wordle,
it isn't necessarily optimal for *Hyper* Wordle.

<!--

Believe it or not, this is a real Wordle variant I ran into back in 2022 [as part of a competition](https://web.archive.org/web/20220521064114/https://botfights.ai/tournament/botfights_iv)
to see who could write the best Wordle solving program. Originally, the competition
tested programs against a sample of 1000 words chosen randomly with replacement.
Since some secret words are easier to solve than others, you could spam submissions repeatedly
with a suboptimal strategy and eventually get lucky enough to beat better strategies:

<img src="/images/wordle/hist.png" style="max-height:50vh; width:auto;"/><br>
*Central limit theory in action.*

Testing against permutations of the 2315 secret words without replacement seemed like
it might negate any chance of abusing variance.
For example, if you used the optimal[^3] [Wordle strategy starting with the word `SALET`](https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle)
(average score of ≈3.4212 guesses) against every secret in the permutation,
submissions would score exactly $$3.4212 \times 2315 = 7920$$ regardless of the permutation
since every potential secret word always appears exactly once. Despite this,
there were still ways to introduce variance:

<img src="/images/wordle/salet-reast-mix.jpg" style="max-height:40vh; width:auto;"/><br>

The histogram above shows the score distribution when using the optimal Wordle strategy
starting with `SALET` (score of 7920) on half of the words in the permutation, and using the second best
strategy starting with `REAST` (score of 7923) on the other half. Variance comes
from the fact that each strategy has its own strengths and weaknesses. For example:
* `SALET` solves `SAUTE` in 2 guesses, while `REAST` solves it in 4.
* `REAST` solves `ROUTE` in 2 guesses, while `SALET` solves it in 4.

If you spam enough submissions, you can retry until you're tested against permutations where words like `SAUTE` end up in the `SALET` half,
and words like `ROUTE` end up in the `REAST` half.

While we could intentionally inject variance like this and spam submit,
there isn't much merit in being the contestant who submits the most times. In particular,
the mixed strategy scores ≈7921.5 on average (the average of `SALET`'s score and `REAST`'s
score) which is worse than `SALET`'s score of 7920 by itself.
What if we could find a way to outperform the `SALET` strategy *on average*? For example,
can we take advantage of the fact that the secrets are permuted *without replacement* to
gain extra information?

-->

## Wacky Trick Leaks Extra State

Before we try to solve a permutation of 2315 words, let's consider a simpler scenario
where we're solving a permutation of six secret words in parallel:
`FIRST`, `DEUCE`, `THIRD`, `FORTH`, `FIFTH`, `SIXTH`. Let's take a look at a strategy
where `LEAKS` is our starting word:

<img src="/images/wordle/leaks-tree.jpg" style="max-height:30vh; width:auto;"/>

This strategy treats each secret independently, meaning our guess for each word is
based solely on feedback we've received for the word so far.<!-- For example, we-->
<!--guess `THIRD` in all three positions where the feedback from the first guess was five gray squares.-->
While we show the secret words in order here, since the strategy treats each secret independently it always
requires a total of 15 guesses to solve all the words regardless of how they're permuted. Next,
consider a strategy with `MAJOR` as our starting word:

<img src="/images/wordle/major-tree.jpg" style="max-height:30vh; width:auto;"/>

Again, this strategy requires 15 guesses to solve any permutation of the 6 chosen secret words.
Neither the `MAJOR` strategy nor `LEAKS` strategy are particularly impressive on their own. Let's
try to solve an unknown permutation of our secret words while mixing the two starting words,
with `MAJOR` for the first three positions and `LEAKS` for the last three:

<img src="/images/wordle/major-leaks-0.jpg" style="max-height:30vh; width:auto;"/>

To put you in the mindset of the puzzle, the actual value of each secret word is kept, well, secret.
The only information you have is that each of the six secret words appears
only once, but can be in any order. The possibilities column lists the possible secret
words which can be in a position based on the feedback from guess 1,
using `1`, `2`, `3`, `4`, `5`, and `6` as shorthand for `FIRST`, `DEUCE`, `THIRD`, `FORTH`,
`FIFTH`, and `SIXTH` respectively.

Before we make any more guesses, is there anything we can do to narrow down the values in
the possibilities column? Looking closely, we already know the position of `2`: it
*must* be in the fourth position since it's the only secret which matches that feedback pattern
for `LEAKS`. This allows us to remove `2` from the lists of possibilities in the first
two positions:

<img src="/images/wordle/major-leaks-1.jpg" style="max-height:30vh; width:auto;"/>

Now that we've removed `2` as a possibility in the first and second positions, we see
the first position must be either `5` or `6`. Consider the following two scenarios:
* If `5` is in the first position, `6` must be in the second position since there would be
  no other option that could go there.
* If `6` is in the first position, `5` must be in the second position since there would be
  no other option that could go there.

In Sudoku[^4] puzzles these are known as [Naked Candidates](https://www.sudokuwiki.org/naked_candidates).
While we don't know which of the two scenarios we're in yet, in every scenario `5` and `6`
must be in the first two positions, allowing us to rule them out from any other position:

<img src="/images/wordle/major-leaks-2.jpg" style="max-height:30vh; width:auto;"/>

After this deduction, we know `1` must be in the fifth position since it's the only viable
option. This allows us to remove it from the list of possibilities for the third
position.

<img src="/images/wordle/major-leaks-3.jpg" style="max-height:30vh; width:auto;"/>

By the same logic, `3` must be in the third position, and we can remove it from the
possibilities for the sixth position.

<img src="/images/wordle/major-leaks-4.jpg" style="max-height:30vh; width:auto;"/>

Finally, we can deduce `4` must be in the sixth position. Initially we only knew the position
of `2`, however after applying deductions we learn the exact position of four out of the six
secrets! If we submit guesses tuned to take advantage of our updated knowledge:

<img src="/images/wordle/major-leaks-solve.jpg" style="max-height:30vh; width:auto;"/>

We're able to solve every word in a total of 13 guesses, an improvement over 15 guesses
for both the `MAJOR` strategy and the `LEAKS` strategy on their own.
Taking a step back, where did this improvement come from? Note that the individual
`MAJOR` and `LEAKS` strategies each have their own strengths and weaknesses:
* `MAJOR` always knows the location of `FORTH` after submitting guess 1, while `LEAKS`
  doesn't find this out until after guess 2.
* `LEAKS` always knows the location of `DEUCE` after submitting guess 1, while `MAJOR`
  doesn't find this out until after guess 2.

In the example we worked through above, notice how the first deduction uses information
from the `LEAKS` half of the puzzle to rule out the location of `DEUCE` (`2`) in
the `MAJOR` half of the puzzle earlier than it normally could. In other words, `LEAKS`' strengths cover for `MAJOR`'s
weaknesses, which in turn gives `MAJOR` enough information to cover `LEAKS`' weaknesses.
By exploiting the asymmetry in the strengths and weaknesses of each strategy,
we're able to iteratively refine both strategies to perform *better* than the sum of their parts!

We can brute force over all $$6! = 720$$ possible permutations
of our secret words to build up histograms showing how much improvement deduction gives us on average:

<img src="/images/wordle/histograms.jpg" style="max-height:30vh; width:auto;"/>

On the left, we have the result of mixing the two strategies without using any deduction
tricks. This produces a vaguely Gaussian looking distribution averaging a score of 15,
the same as using `MAJOR` or `LEAKS` on their own. Note that variance comes from the
fact that `MAJOR` and `LEAKS` each have their own strengths and weaknesses:
* The score is lower for permutations where secrets `MAJOR`/`LEAKS` solve quickly are shuffled into their halves.
* The score is higher for permutations where secrets`MAJOR`/`LEAKS` solve slowly are shuffled into their halves.

On the right, we have the result of mixing the two strategies and using
deduction tricks to refine our guesses with an average score of 13.9, a 1.1 point improvement!

## Widen Scope

Now that we've seen this work with permutations of six secret words, let's see how we
do against permutations of the complete list 2315 secret words. We can start off by mixing
the best Wordle strategy starting with `SALET` (score of 7920) with the second best strategy starting with
`REAST` (score of 7923):

<img src="/images/wordle/salet-reast-hist.jpg" style="max-height:40vh; width:auto;"/>

The values on the right are show the score distribution of the `SALET`/`REAST`
mixed strategy on 1000 random permutations of the 2315 secret words without any deduction.
On the left we have the results on the same 1000 permutations after eliminating possible
states via deduction each turn and refining our guessing strategy accordingly. Deduction takes our
average score from ≈7921.5 to ≈7768.8, a 150 point improvement!

`SALET` and `REAST` were chosen since they're the top two Wordle strategies,
but what about mixing other strategies? During the competition, the best combination of
strategies I found was by assigning 10% of the permutation to each of the top 10
Wordle starting words: `SALET`, `REAST`, `CRATE`, `TRACE`, `SLATE`, `CRANE`, `CARLE`, `SLANE`, `CARTE`,
and `TORSE`. Plotting this against the previous two histograms:

<img src="/images/wordle/top-10-hist.jpg" style="max-height:40vh; width:auto;"/>

The top 10 mix with deduction is shown in green with an average
score of ≈7628.0, an additional 130 point improvement over the `SALET`/`REAST` deduction strategy!
Trying to mix in more words (e.g. top 20) seems to have diminishing returns since introducing
less efficient starting words drags the expected score without deductions up.
The top 10 mixed strategy is what I ultimately used in the competition mentioned earlier, [winning
with a score of 7574](https://web.archive.org/web/20220628055213/https://botfights.ai/leaderboard/botfights_iv?results=1)
-- a ≈4.4% improvement over the optimal Wordle strategy by itself!

## Bonus Trick

While proofreading the diagrams for the smaller 6-secret word case, I realized there's
a second deduction strategy commonly known as [Hidden Candidates](https://www.sudokuwiki.org/hidden_candidates)
which is "dual" to the Naked Candidates trick. Going back to the diagram:

<img src="/images/wordle/major-leaks-0.jpg" style="max-height:30vh; width:auto;"/>

Given the feedback from guess 1, notice there's only 1 possible location where `4` can go,
meaning `4` must be in the 6th position:

<img src="/images/wordle/major-leaks-hidden-1.jpg" style="max-height:30vh; width:auto;"/>

After updating the possibilities in the 6th position, notice that the only valid location
for `3` is in the third position, meaning it must be there:

<img src="/images/wordle/major-leaks-hidden-2.jpg" style="max-height:30vh; width:auto;"/>

And so on. After generalizing this trick for subsets of N words with only N possible locations,
we can incorporate it into the top 10 mixed strategy to squeeze out some extra performance:

<img src="/images/wordle/hidden-deductions-hist.jpg" style="max-height:40vh; width:auto;"/>

This takes our average from ≈7628.0 to ≈7598.3, averaging a 320 point improvement over
the best Wordle strategy's score of 7920. To put this into perspective, this is the same
as the amount improvement between the best Wordle strategy and the [3334th best Wordle strategy](https://github.com/alex1770/wordle/blob/main/normal.some3593.proven#L3334)!

## Final Words

If you want to tinker with ideas, I
generated all the data for the strategy histograms in this post using [this very adhoc Rust code](https://github.com/ckw017/hyper-wordle).
Some interesting open questions are:
* What's the best mix of two starting words (i.e. lowest average score)? Intuitively,
  some starting words might "synergize" with each other better than others if
  the structure of their decision trees tend to lead to more deductions.
* My winning strategy only behaves non-deterministically on the first turn, when we randomly
  use 10 different guesses despite every word having identical feedback at that point (i.e.
  no feedback). Can we get further improvements by behaving non-deterministically on later
  turns?
* The deduction strategy only removes words from the possibility pool when we're *certain*
  they must be somewhere else. Is there a way to "fuzzily" refine our possibilities
  to values other than 0, e.g. "this word is likely to be in position A,
  so it's less likely to be in position B"?
* In the version of Hyper Wordle played in this writeup, each batch of 2315 guesses can contain duplicates.
  What do strategies look like if we don't allow duplicates?
* Are there any other games/scenarios where combining multiple suboptimal strategies outcompetes
  a strategy which would normally be stronger?
* Should I find less convoluted things to do with my free time?

If you enjoyed reading this, this entire writeup was actually much longer before
I broke it into three standalone parts. Excluding the one you're reading right now, the other two
are:
* [The Sixteen Bottles of Wine Riddle](/2025/08/11/Wine/) -- I thought of this riddle while trying to think of a
  simpler version Hyper Wordle to use as a toy example to introduce some concepts. Despite
  trying to make it as simple and symmetric as possible, it still ended up having a surprising
  amount of depth!
* [Writing Wordle bots for fun and profit](/2025/08/23/Wordle/) -- This gives some context
  on some of the other stages of the Wordle strategy competition, which I also happened
  to win. No novel discoveries to share there, but it's a fun story anyway if you're into
  Wordle.

Anyway, thanks for reading!

<!--

The example given only considers mixing two strategies, however my best submission involved mixing the ten best strategies and sharing information between them, netting a score of 7574, a 4.4% improvement over the best performance for a single deterministic strategy. I found mixing more than ten strategies started to yield diminishing returns. Possible explanations for this are:
* As we introduce more strategies, we need to involve "worse" starting words (strategies in the top 10 are mostly good, strategies in the top 50 not so much). This makes it harder for the new strategy to reveal enough useful information to other strategies to compensate for how bad it is in isolation
* The more strategies we introduce, the lower the chance any single strategy has enough "samples" to reveal actionable information

## Open questions

Anyway, this was enough to secure the win for the final Wordle competition, and leads to some interesting open questions:
* The information sharing strategy described only removes words from the pool of strategy if we're *certain* that the word is already somewhere else. In reality, you might be able to determine the probability a word is somewhere based on how many valid spots it can be in, and use this information when doing the next round's guesses.
* What's the best mix of two starting words (nets lowest expected number of guesses)? I imagine this is harder than just mixing the two best strategies -- some strategy pairs might have better "synergy", i.e. reveal information others might find "useful" more frequently. For what it's worth, I'm pretty sure computing this exactly is extremely intractable, but I'm frequently wrong about this sort of thing.
* What's the optimal mix of any number of starting words? (Probably super-duper intractable)
* My last submission only mixed strategies during the first turn. Can we do better by mixing strategies on other turns as well?
* Other than the information sharing at the end of each round, the strategies act entirely independently. Can the strategies somehow leverage knowledge about what the other strategies will do to adjust their own guesses, essentially betting the other strategies are likely to uncover extra info?
* Are there any other games/scenarios with analogous properties to this kind of Wordle, i.e. where running multiple suboptimal strategies outcompetes a single strategy?
* Should I find less convoluted things to do in my free time?

-->

---

[^1]:
    2315 was the original number of possible secret words before being acquired by the New York Times. According
    to the NYT [Wordle FAQ](https://www.nytimes.com/interactive/2024/02/16/upshot/wordlebot-faq.html)
    there are now 3200 secret words.

[^2]:
    12972 was the original number of valid Wordle guess words. After the New York Times acquired
    Wordle, it was [increased to 14855](https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle,_part_2).

[^3]:
    Leading with `SALET` was the best strategy in early 2022, but since the New York Times changed
    the word list and secret list after acquiring Wordle, it is [no longer optimal](https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle,_part_2#Updated_best_starting_words_using_New_York_Times_word_lists_as_of_30_August_2022).

[^4]:
    You can think of the deduction steps between guesses as very oblong Sudoku puzzles,
    where instead of a 9x9 grid with uniqueness constraints on 1 to 9, you have a
    2315x1 line with uniqueness constraints on 1 to 2315.
