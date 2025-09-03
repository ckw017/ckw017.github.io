---
layout: post
img: /images/pkmn/sportball.png
title: Pokémon or startup?
excerpt_separator: <!--more-->
---

<a href="https://www.sporcle.com/games/netcat/pokemon-or-startup-quiz" target="_blank" rel="noopener noreferrer">![](/images/pkmn/sporcle.jpg)</a><br>
*If you want to take the quiz you can find it <a href="https://www.sporcle.com/games/netcat/pokemon-or-startup-quiz" target="_blank" rel="noopener noreferrer">here</a>, the*
*rest of this post describes how names were chosen and contains spoilers for the answers.*
<!--more-->

A while back a friend showed me [a quiz](https://www.bizjournals.com/boston/pulse/quiz/is-it-a-drug-or-is-it-a-pokemon/15969731)
posing the age old question: is it a Pokémon, or a pharmaceutical drug? The quiz
is surprisingly challenging, possibly because both drug names and Pokémon names
attempt to take biology terminology and make it sound cute and marketable. There's
no shortage of quizzes like these either, for example:
* [Pokémon or Cheese?](https://www.sporcle.com/games/hellofromUK/pokecheese)
* [Pokémon or IKEA furniture?](https://www.sporcle.com/games/Minibiggles/pokmon-or-ikea-furniture)
* [Pokémon or Big Data?](https://pixelastic.github.io/pokemonorbigdata/)
* [Pokémon or RuPaul's Drag Race?](https://www.sporcle.com/games/Qaqaq/rupoke)

You may have also seen this meme:

<a href="https://youtu.be/0hR4peP9V4A?si=0WSqu63v4ko5U_WK&t=66" target="_blank" rel="noopener noreferrer">![](/images/pkmn/recruiting.jpg)</a><br>(I see a total of seven Pokémon.)

While putting together my own quiz it occured to me that instead of spending half
an hour manually skimming through hundreds of Pokémon and startup names, I could spend several hours trying to get a computer to do it for me.
To do this we would need some kind of statistical model of natural language to quantify
how much a name sounds like it would be a Pokémon or startup -- farfetch'd right?
Conveniently, it just so happens a handful of obscure tech companies and researchers have
quietly advanced the state of the art for language modeling over the last few years.

## LLMs and confidence

One approach would be to ask an LLM directly how likely it thinks each word is in one
category or another. For example:

> **Prompt**: Does "[Beartic](https://bulbapedia.bulbagarden.net/wiki/Beartic_(Pok%C3%A9mon))" sound like a Pokémon or a tech startup? Respond with one of: "Pokémon" or "Tech Startup" and state your confidence as a percentage.
>
> **Llama 3.2**: Pokémon, 80%

While we could take this at face value, keep in mind the LLM isn't
doing any "introspection" on its own internal workings to come up with "80%", but rather
states a level of confidence that the model would expect to appear in this context. It's a subtle
distinction, but consider what happens if you ask the model a few more times, clearing
the context window between attempts:

> **Llama 3.2**: Pokémon (80%)<br>
> **Llama 3.2**: Tech Startup (80%)<br>
> **Llama 3.2**: Tech Startup (70%)<br>
> **Llama 3.2**: Pokémon, 70%<br>
> **Llama 3.2**: Tech Startup. 80%<br>

Despite outputting "Pokémon, 80%" earlier, the odds of it responding
with Tech Startup or Pokémon seem closer to 50/50. Also note that regardless of which option it picks,
it always claims 70% or 80% confidence in its answer[^1]. If we can't trust the LLM's
own evaluation of its confidence, how can we measure it? Rather than asking the model
about it's confidence and relying on its response, we can look directly at the
underlying probability distribution that the model samples tokens from. Rerunning with
[logprobs](https://cookbook.openai.com/examples/using_logprobs)
enabled, the top 5 options for the first token are:


<!-- It's a subtle distinction, but consider the simpler case of flipping a coin:

> **Prompt**: Toss a fair coin. Respond with one of: "Heads" or "Tails" and state the probability of the outcome as a percentage.
>
> **Llama 3.2**: Heads, 50%

While almost every LLM will state that the odds of each side of the coin are 50%,
in practice [LLMs are biased towards heads upwards of 70% of the time](https://rnikhil.com/2025/04/26/llm-coin-toss-odd-even).
If we can't trust the accuracy of the LLM's response, how can we gauge its confidence?
Rather than asking the model about it's confidence and checking its response, we can instead
look directly at the underlying probability distribution that the model samples tokens
from. Rerunning with [logprobs](https://cookbook.openai.com/examples/using_logprobs)
enabled, the top 5 options for the first token are: -->

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


| **First Token**  | **logprob**         | $$\textbf{e}^\textbf{logprob}$$
|:-----------|---------------------|---------------:|
| `Tech`     | -0.45017755         | 63.75% |
| `Pok`      | -1.1627344          | 31.26% |
| `Be`       | -4.1083674          | 1.64% |
| `Startup`  | -4.659017           | 0.95% |
| `Start`    | -4.826072          | 0.80% |

Based on the first token, it appears the model has a 63.75% chance of responding with
"**Tech** Startup", and a 31.26% chance of responding with "**Pok**émon[^2]. The remaining
5% of the time the model ignores our instruction to respond only with "Tech Startup" or
"Pokémon", which for the sake of simplicity we will ignore. Excluding answers
that don't fit the expected format and normalizing, we find that the model answers
"Tech Startup" 67.11% of the time, and "Pokémon" 32.89% of the time.

## Results

<img src="/images/pkmn/applin.png" style="max-width: 20%">
<img src="/images/pkmn/silicobra.png" style="max-width: 20%">
<img src="/images/pkmn/klang.png" style="max-width: 20%">
<img src="/images/pkmn/grubbin.png" style="max-width: 20%"><br>*Applin, Silicobra, Klang and Grubbin.*

Now that we can measure how likely an LLM is to categorize a name as
a Pokémon or a startup, we can go through lists of both categories and search for good candidates for the quiz. In
order to make the quiz as difficult as possible, we want to find Pokémon that sound like
they could be a startup, and startups that sound like they could be a Pokémon.
For the list of Pokémon, I included everything up to [Sword and Shield](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Sword_and_Shield)
(2019), since the next major releases [Scarlet and Violet](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Scarlet_and_Violet) (2022)
came out fairly close to Llama 3's knowledge cutoff date. Our top 15 are:

| **Name**    | **Pokémon** | **Tech Startup** |
|:------------|---------|--------------|
| [Applin](https://bulbapedia.bulbagarden.net/wiki/Applin_(Pok%C3%A9mon))      | 12.69%  | 87.31%       |
| [Electrode](https://bulbapedia.bulbagarden.net/wiki/Electrode_(Pok%C3%A9mon))   | 16.04%  | 83.96%       |
| [Melmetal](https://bulbapedia.bulbagarden.net/wiki/Melmetal_(Pok%C3%A9mon))    | 23.45%  | 76.55%       |
| [Dottler](https://bulbapedia.bulbagarden.net/wiki/Dottler_(Pok%C3%A9mon))     | 26.49%  | 73.51%       |
| [Silicobra](https://bulbapedia.bulbagarden.net/wiki/Silicobra_(Pok%C3%A9mon))   | 26.75%  | 73.25%       |
| [Corvisquire](https://bulbapedia.bulbagarden.net/wiki/Corvisquire_(Pok%C3%A9mon)) | 26.82%  | 73.18%       |
| [Polteageist](https://bulbapedia.bulbagarden.net/wiki/Polteageist_(Pok%C3%A9mon)) | 27.13%  | 72.87%       |
| [Eelektrik](https://bulbapedia.bulbagarden.net/wiki/Eelektrik_(Pok%C3%A9mon))   | 27.23%  | 72.77%       |
| [Arctozolt](https://bulbapedia.bulbagarden.net/wiki/Arctozolt_(Pok%C3%A9mon))   | 28.63%  | 71.37%       |
| [Morgrem](https://bulbapedia.bulbagarden.net/wiki/Morgrem_(Pok%C3%A9mon))     | 29.85%  | 70.15%       |
| [Hattrem](https://bulbapedia.bulbagarden.net/wiki/Hattrem_(Pok%C3%A9mon))     | 30.10%  | 69.90%       |
| [Volbeat](https://bulbapedia.bulbagarden.net/wiki/Volbeat_(Pok%C3%A9mon))     | 30.11%  | 69.89%       |
| [Thievul](https://bulbapedia.bulbagarden.net/wiki/Thievul_(Pok%C3%A9mon))     | 30.41%  | 69.59%       |
| [Armaldo](https://bulbapedia.bulbagarden.net/wiki/Armaldo_(Pok%C3%A9mon))     | 30.77%  | 69.23%       |
| [Klang](https://bulbapedia.bulbagarden.net/wiki/Klang_(Pok%C3%A9mon))       | 31.48%  | 68.52%       |

This list mostly makes sense to me other than Polteageist[^3], Morgrem and Hattrem.
Looking closely, those three and six others (Applin, Dottler, Silicobra, Corvisquire, Arctozolt, and Thievul) all come
from the most recent games included in the dataset, [Sword and Shield](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Sword_and_Shield).
I suspect since newer Pokémon appear less frequently
in Llama 3's training data, they're more likely to be confused for a startup than older, well-known Pokémon like
Pikachu or Charizard. Some highlights for me are:
* [Silicobra](https://bulbapedia.bulbagarden.net/wiki/Silicobra_(Pok%C3%A9mon)), which is so straightforward ("silicon" + an animal) it almost sounds like it was made up just for the quiz.
* [Applin](https://bulbapedia.bulbagarden.net/wiki/Applin_(Pok%C3%A9mon)), which I initially thought was ranked highly because of Apple, only to realize it could also be a play on software "apps".
* [Klang](https://bulbapedia.bulbagarden.net/wiki/Klang_(Pok%C3%A9mon)), which is robotic sounding but also remniscent of abbreviations for "programming language" like in [Clang](https://en.wikipedia.org/wiki/Clang), [Erlang](https://en.wikipedia.org/wiki/Erlang_(programming_language)) and [Golang](https://en.wikipedia.org/wiki/Go_(programming_language)).
* Honorable mention to [Grubbin](https://bulbapedia.bulbagarden.net/wiki/Grubbin_(Pok%C3%A9mon)) in 16th place, which sounds like it could be yet another food delivery or meal kit startup.

Switching our attention to startups that sound like Pokémon, I took startup names
from [this dataset](https://www.kaggle.com/datasets/sashakorovkina/ycombinator-all-funded-companies-dataset?select=companies.csv)
of [Y Combinator](https://www.ycombinator.com/) backed companies. Our top 15 are:

| **Name**      | **Pokémon** | **Tech Startup** |
|:----------|---------|--------------|
| [Ditto](https://www.ycombinator.com/companies/ditto)     | 85.89%  | 14.11%       |
| [Wren](https://www.ycombinator.com/companies/wren)      | 73.82%  | 26.18%       |
| [Koala](https://www.ycombinator.com/companies/koala)     | 72.13%  | 27.87%       |
| [Protego](https://www.ycombinator.com/companies/protego)   | 70.91%  | 29.09%       |
| [Nexu](https://www.ycombinator.com/companies/nexu)      | 70.30%  | 29.70%       |
| [Manatee](https://www.ycombinator.com/companies/manatee)   | 70.24%  | 29.76%       |
| [Hedgehog](https://www.ycombinator.com/companies/hedgehog)  | 69.57%  | 30.43%       |
| [Hedgehog](https://www.ycombinator.com/companies/hedgehog-2)  | 69.57%  | 30.43%       |
| [Remora](https://www.ycombinator.com/companies/remora)    | 68.75%  | 31.25%       |
| [Wasp](https://www.ycombinator.com/companies/wasp)      | 68.52%  | 31.48%       |
| [Okani](https://www.ycombinator.com/companies/okani)     | 68.51%  | 31.49%       |
| [Platypus](https://www.ycombinator.com/companies/platypus)  | 66.89%  | 33.11%       |
| [Lollipuff](https://www.ycombinator.com/companies/lollipuff) | 65.26%  | 34.74%       |
| [Corgi](https://www.ycombinator.com/companies/corgi)     | 65.14%  | 34.86%       |
| [Skyvern](https://www.ycombinator.com/companies/skyvern)   | 62.58%  | 37.42%       |

The number one spot goes to [Ditto](https://www.dittowords.com/), a startup making
devtools for localization and legal copy. This makes sense, since it's also literally
the [name of a Pokémon](https://bulbapedia.bulbagarden.net/wiki/Ditto_(Pok%C3%A9mon)).
Most of the other spots are filled by the names of real life animals, including two different
startups named Hedgehog: one that tried to make ["a crypto robo-adviser"](https://www.ycombinator.com/companies/hedgehog)
and one working on ["robotic mushroom farms"](https://www.ycombinator.com/companies/hedgehog-2).
Cleaning up the dataset to remove literal animals and Pokémon, we get:

| **Name**      | **Pokémon** | **Tech Startup** |
|-----------|---------|--------------|
| [Protego](https://www.ycombinator.com/companies/protego)   | 70.91%  | 29.09%       |
| [Nexu](https://www.ycombinator.com/companies/nexu)      | 70.30%  | 29.70%       |
| [Okani](https://www.ycombinator.com/companies/okani)     | 68.51%  | 31.49%       |
| [Lollipuff](https://www.ycombinator.com/companies/lollipuff) | 65.26%  | 34.74%       |
| [Skyvern](https://www.ycombinator.com/companies/skyvern)   | 62.58%  | 37.42%       |
| [Inkling](https://www.ycombinator.com/companies/inkling)   | 62.27%  | 37.73%       |
| [Linkana](https://www.ycombinator.com/companies/linkana)   | 62.12%  | 37.88%       |
| [Bristle](https://www.ycombinator.com/companies/bristle)   | 62.11%  | 37.89%       |
| [Trébol](https://www.ycombinator.com/companies/trebol)    | 61.01%  | 38.99%       |
| [Usul](https://www.ycombinator.com/companies/usul)      | 58.58%  | 41.42%       |
| [Flike](https://www.ycombinator.com/companies/flike)     | 58.29%  | 41.71%       |
| [Markhor](https://www.ycombinator.com/companies/markhor)   | 58.25%  | 41.75%       |
| [Balto](https://www.ycombinator.com/companies/balto)     | 56.74%  | 43.26%       |
| [Hazel](https://www.ycombinator.com/companies/hazel-2)     | 55.91%  | 44.09%       |
| [Wolfia](https://www.ycombinator.com/companies/wolfia)    | 55.89%  | 44.11%       |

Some highlights for me:
* [Lollipuff](https://www.ycombinator.com/companies/lollipuff), a luxury goods auction service, which sounds like it would fit right in with Pokémon like [Igglybuff](https://bulbapedia.bulbagarden.net/wiki/Igglybuff_(Pok%C3%A9mon)), [Jigglypuff](https://bulbapedia.bulbagarden.net/wiki/Jigglypuff_(Pok%C3%A9mon)), [Wigglytuff](https://bulbapedia.bulbagarden.net/wiki/Wigglytuff_(Pok%C3%A9mon)), and [Jumpluff](https://bulbapedia.bulbagarden.net/wiki/Jumpluff_(Pok%C3%A9mon)).
* [Skyvern](https://www.ycombinator.com/companies/skyvern), an "open source AI agent" not to be confused with [Noivern](https://bulbapedia.bulbagarden.net/wiki/Noivern_(Pok%C3%A9mon)) and other Flying/Dragon type Pokémon.
* [Inkling](https://www.ycombinator.com/companies/inkling), a "collective intelligence solutions" service which sounds like it could be a squid or an octopus Pokémon, and shares a name with the mascots of [a different Nintendo franchise](https://splatoon.fandom.com/wiki/Inklings).

## Final thoughts

I came up with this idea on a whim and it worked out surprisingly well. If you want
to play around with your own ideas, everything was done with a [llama.cpp](https://github.com/ggml-org/llama.cpp) and a simple
Python script uploaded [here](https://github.com/ckw017/pokemon-or-startup). Anyway, thanks for reading!

---

[^1]:
    My best guess for why the confidence is in the 70% to 80% range regardless of the choice
    is people are more likely to publicly share opinions or guesses they're confident
    about, leading to selection bias in the training data. I'm about 70% confident in this
    theory.

[^2]:
    These percentages assume that the LLM's [temperature](https://medium.com/@kelseyywang/a-comprehensive-guide-to-llm-temperature-%EF%B8%8F-363a40bbc91f) parameter is set to 1. If it's less than
    1, it would favor "Tech Startup" even more.

[^3]:
    I ended up removing Polteageist and adding Grubbin (16th place) in the quiz. I
    suspect it was labeled confidently as a startup not because it sounds like a startup,
    but because "poltergeist possessing a pot of tea" sounds ridiculous even for a Pokémon.

<!--
We can get a feel for this problem by asking the LLM a simpler question: [heads or tails](https://rnikhil.com/2025/04/26/llm-coin-toss-odd-even)?

> **Prompt**: Toss a fair coin. Respond with one of: "Heads" or "Tails" and state the probability of the outcome as a percentage.
>
> **Llama 3.2**: Heads, 50%

That sounds reasonable, but what happens if we ask a few more times?[^1]

> **Llama 3.2**: Heads 50%<br>
> **Llama 3.2**: Heads (50%)<br>
> **Llama 3.2**: Heads, 50%<br>
> **Llama 3.2**: Heads (50%)<br>
> **Llama 3.2**: Heads (50.0%)<br>
> **Llama 3.2**: Heads 50%<br>
> **Llama 3.2**: Tails - 50.0%<br>
> **Llama 3.2**: \*\*Heads\*\* (50%).\n\nWould you like to simulate another coin toss?<br>
> **Llama 3.2**: Tails, 50%<br>
> **Llama 3.2**: Heads (50%)<br>

It seems like the model has a bias towards reporting "Heads" in our sample
size of 10. While we could increase the sample size to see if a pattern
emerges, it might be more insightful to look directly at the distribution the model is sampling
from. Rerunning with [logprobs](https://cookbook.openai.com/examples/using_logprobs)
enabled, the top 5 options for the first token are:

<style>
table{
    border-spacing: 50px;
    border:1px solid #000000;
}

th {
    border: 1px solid #000000;
    padding: 5px;
    max-width: 40vw;
}

td{
    border:1px solid #000000;
    padding: 5px;
    max-width: 40vw;
}
</style>

| **Token 1**   | **logprob**            |
|----------|-------------------:|
| `He`     | -0.4107096 (66.3%) |
| `T`      | -1.8492415 (15.7%) |
| `**`     | -1.9469111 (14.3%) |
| `Result` | -4.807211  (0.8%)  |
| `The`    | -5.658432  (0.3%)  |

Based on the first token it appears the model is biased towards saying
"**He**ads" 66.3% of the time, and "**T**ails" 15.7% of the time, although we can't be totally sure yet. For example:
* `He` might be the start of "**He**y look, it landed on Tails".
* `T` might be the start of "**T**he coin landed on Heads".
* `**` is the LLM adding bold formatting to it's answer, however we don't if the answer is heads or tails yet.

To remove ambiguity, we can feed the first token options back into the LLM and examine the logprobs
for the next tokens:


| **Tokens**         | **logprob 1**          | **logprob 2**           | **Joint Probability** |
|----------------|------------------:|--------------------:|------------------:|
| `He`, `ads`    | -0.4107096 (66.3%) | -0.000002  (100.0%) | 66.3%             |
| `T`, `ails`    | -1.8492415 (15.7%) | -0.0000839 (100.0%) | 15.7%             |
| `**`, `He`     | -1.9469111 (14.3%) | -1.0628203 (34.5%)  | 4.9%              |
| `**`, `Result` | -1.9469111 (14.3%) | -1.2099322 (29.8%)  | 4.3%              |
| `**`, `T`      | -1.9469111 (14.3%) | -1.3429335 (26.1%)  | 3.7%              |


| **Token 1**  | **Token 2** | **Joint Probability** |
|--------------|------------------|-------------------|
| `He` (66.3%) | `ads` (100.0%)   | 66.3%             |
| `T` (15.7%)  | `ails` (100.0%)  | 15.7%             |
| `**` (14.3%) | `He` (34.5%)     | 4.9%              |
| `**` (14.3%) | `Result` (29.8%) | 4.3%              |
| `**` (14.3%) | `T` (26.1%)      | 3.7%              |

When `He` or `T` are output as the first token, the next token is
practically guaranteed to be `ads` or `ails` to form `Heads` or `Tails` respectively. For
`**`, the odds of the next token are roughly split between `He`, `T`, and `Result`.
We can continue feeding in ambiguous results and examining logprobs to form a tree structure representing
the different sequences of tokens the LLM might output:

<img src="/images/pkmn/heads-tails-sankey.jpg" style="max-height:50vh;"><br>*Diagram made with [Sankeymatic](https://sankeymatic.com/build/?i=PTAEFEDsBcFMCdQDEA2B7A7gZ1AI1tBrLJKAHJoAmsWANKCgJYDWso0AFo1gFwBQIUEOHCAymgCu8AMZsA2gEEAsgHkAqmQAqAXVCaAhvADmBPnwA8o6IegA%2BUHIBsjgHQBmXQAk2AYjcBWfQsrG3s5AEZ%2DFwB2XU1QH30A4Ot4OwdwgBZ3XQAqXIT9QJTQhzcY3XMVTgR7RP0gvm8HZxzQb31KHD9ivniIqNi9fUYUbqT%2DM3yHbIBOPNzmnqDpuXKh%2DPjE5NXsj1B8gCUaCRRoQuLV8JdMhaqa%2BDqGxvzmuTmFjq6EgJXc%2DvWCwMo3GyT4RxOZwcACYbgtjlhTtAeO1YJ1ur9wbkEUiMi5HPDIci9IUdtiiQ4AAxtCGIs48cxoB5PBpTcl04n9a4Eg7spEo4FjUmTPg8JaYsVo77LUWvXwSuXon7FHi0%2DmopUy1UFRIqtVQ3VBBkhNJPXo8LYTWX%2DYXWnH0knbSba%2B2ckZCp2iwWg52bd0%2BsyCADq%2BhMOAGlMpugAQhJKCZoAIwNUOAgYf4o6BY%2DHTEms3GEzMM3F9AAPGh57OF97QzOeSRYRiQIyVgsEGaR3RINBUVs585yaH%2BfxxeD6SBYAAOaDS%2BmgjDQkEDYAAmpJQNJx6AsO39OQqLAAOQ4aRodDwehMVjsLi8PM8KvtnyU%2DzRPMiD9CFzfmegPen89QAAM1%2DPdG2bFA2FQTB%2BEER8B3CRxMxTNMyFgWQsEbecaASJDHGXUAACI5FybRCNAABbNEJyItQdz%2DSAAE8%2DwoyQYAYWAgPONAADcEEI2CwHghxSNAUR9B4psjCwAi6LYGoN0XaB4DPHB8HQDB2DQDcJCwaA0AoxgAC9YDzRjJEQShGFDMcKOPP9J0nNEx0gWRvxcPhGxM0BNIADkjPhQA4UAkMpPgKMMIwmwYUBwmhQLEDiwLznCXzAtwUBaz4XAjEUwCfGoSgiqCdgXKnQwSHOMg%2BEgA8fNi%2BKgtADNAvK6QpNAaJJjwGdqEQMKb1gKjQFqyBTLy38fF86aZsCtBJ30droGY8I%2BCAjSdPgHi5ykNhqWcQKm1TeBGGgICVIo0BJGgRtqAAWibQKAMm2ZXreuaFqW5jqUmFB9HMiRuPgPrQFgUtFsTUAACtdPnIDzJOqKaOq6HYcYeGSG%2BFH4FgPj4B3Iwx0nYKUbnaxpC4VyDMnSC4D07SxoqvS%2BD%2B9STzPSbIy5gauGochAq4IwOCYIXzmpLrApAmAgMWtgsHHLA7p3E6gMCpgxrajrqUanG%2DvnPivLYcJwgGiKjEgdGVoC1nYBQSB9GG%2DRHOcnAV1a4yjfwnzYEYUXQEya39HU7aUAkNgnacwxXcl04UEnHH2sbRdQDd0BpywhdSHUzBAqIX2OHOAOwptuO0Az5P9EBtB9BF0gBqwCmhvDqvJcYfHznwECcfSnH9GYacm3OfCQ7D4CZwi85D1oFxD0C%2BPOMYUtQEPWftwkICgMX5fZ5qKi0A3ndzj3L2MoG6RQAGygL%2DCgg9yomBM%2DlyBWEYifGHP1OmD0xgKNwGvxwwincKvE2DNGpJGaEmRoT0HAdCRwbg3DAL4hqb44DKTQIvi4SkmRogS1Ysg%2BIlJ6B3XAVA18SC2DegvsQ2BsxsEUN5KAEhWDKQIMyDQrBsx%2DCzFWvgtgcpqFMPAdENwlJeEgN5F8HAzCXwZlmBwykSFIEMM2IImR0RZi%2BUyCo%2D4%2DohFYP8FotwCjoiUlwTo10ajwG%2BVmPFPhvJXQoikfol8jhoiOBMdETIswGH3GOvYdRjhfIYLCvY%2DIfjaguN8l1cICjXxuHwmEvkDp4gyP8G4KBJiAhviSY44YIJ9FZH8JArJ5DclEgZEyfxVisGOC4UAA).*

Here I've colored the branches of the tree where the LLM would output "Heads" in blue, the branches where
it would output "Tails" in red, and the branches I was too lazy to squeeze into the visualization
labeled as "&lt;Other&gt;" in gray. Summing up the leaves of the tree we see the LLM
outputs "Heads" at least 73.6% of the time, and "Tails" at most "26.4%" of the time[^1],
contradicting its own claim that it picks heads and tails each with 50% probability.

Llama 3.2's bias towards outputting heads is likely an artifact of human bias to
write "Heads" in coin toss scenarios within the training data. While capturing biases in the training set isn't great
for trying to simulate a fair coin, it's perfect for our purpose of estimating how likely
a person is to mix up a Pokémon name with a startup name.

Returning to our example from earlier, we can prompt the LLM directly without asking for it's confidence:

> **Prompt**: Does "Beartic" sound like a Pokémon or a tech startup? Only respond with one of: "Pokémon" or "Tech Startup".
>
> **Llama 3.2**: Pokémon
-->


<!--
[^1]:
    Each of these samples were taken from fresh prompts to the LLM, not as part of a single
    conversation. When asked repeatedly in a single conversation, some LLMs do something akin to the
    Gambler's Fallacy and [outputs flips that would even the distribution](https://medium.com/%40gathright/llms-cant-flip-a-fair-coin-but-they-seem-to-know-the-odds-06b5ccf2cc2c).
-->
