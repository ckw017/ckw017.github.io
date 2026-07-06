---
layout: post
img:  /images/dodecahedra/thumbnail2.jpg
title: Incomplete Open Dodecahedra
unlisted: false
highlight: true
excerpt_separator: <!--more-->
---

I have a secret. Don't tell anyone, but after majoring in Computer <i><u>Science</u></i> and Data <i><u>Science</u></i> at Berkeley's College of
Letters and <du><i>Sciences</i></du> I somehow ended up with a Bachelor of
$${\color{#dd2222}A}{\color{#dd8800}\mathfrak{r}}{\color{#00aa00}\mathfrak{t}}{\color{#0000ff}\mathfrak{s}}$$. Anyway, it was thanks to
a required art class that I first encountered [*Incomplete Open Cubes*](https://www.sfmoma.org/artwork/97.516.A-KKKKKKKKKK/) by Sol LeWitt at
San Francisco's Museum of Modern Art:

<!--more-->

<center><img src="/images/dodecahedra/moma.jpg" style="max-height:50vh"></center>

The main idea behind the installation is to explore "all of the ways of not making a cube." In
other words, the structures comprise every way to combine up to 12 edges of a cube such that:
* All of the edges are connected.
* At least one edge is missing.
* The structure is 3-dimensional (the edges aren't all part of the same face).
* Each structure is unique, treating rotations as equivalent.

After admiring the piece for a few minutes, I was inspired in the form of the
following syllogism I'm sure many other modern art museum visitors have experienced:

* Art is created by artists.
* I am not an artist.
* Hey wait, I could've done that!
* Therefore, it is not art.

The caveat here is even if I could've done it, I sure didn't, and even if I did,
I sure wouldn't be the first. Of course nothing's stopping us from upping the original!

# Keeping things Platonic

<center>

<img src="/images/dodecahedra/six.jpg" style="max-height:40vh"><br>

<i>"The Six Platonic Solids" by James Arvo and David Kirk.<br>
From left to right, back to front: Dodecahedron, Teapotahedron, Icosahedron, Cube, Tetrahedron, and Octahedron.</i>
</center>

The cube is a member of a group of shapes known as the [Platonic Solids](https://en.wikipedia.org/wiki/Platonic_solid),
a group of "regular" polyhedra where every edge is the same length, every face is the same
regular polygon, and every vertex has the same number of faces meeting.
Logically, in order to flex on Sol LeWitt's *Incomplete Open Cubes* we'd want to replace the cubes with a more
complicated platonic solid, either a dodecahedron, icosahedron, or teapotahedron. I went
with the dodecahedron since it seemed natural to progress
from 4-sided faces to 5-sided faces.

<center><a href="https://daskunstbuch.at/2013/01/07/ausstellungskatalog-kunstlermonographie-sol-lewitt-centre-pompidou-metz-m-museum-leuven-2012/" target="_blank"><img src="/images/dodecahedra/notes.jpg" style="max-height:40vh"></a><br>
<i>Sol LeWitt's notes for Incomplete Open Cubes.</i>
</center>

Sol LeWitt originally planned his installation by hand in a notebook, manually drawing out different combinations
of edges and verifying they meet all the conditions. Since cubes have 12 edges and each edge is either
present or not, there are a total of 2^12 = 4096 possible combinations of cube edges which
potentially needed to be checked for *Incomplete Open Cubes*. If we swap cubes for dodecahedra,
we'll need to account for 30 edges, i.e. 2^30 ≈ 1 billion total combinations.
Exploring these by hand would be orders of magnitude more tedious, so we'll need to find a way to automate the process somehow.

# 30 bits ought to be enough for anybody

If we want to write a program to search for valid structures, a natural way to represent
each set of edges is as a 30-bit integer. By numbering each of the edges in a dodecahedron,
we can set the corresponding bit to 1 if the edge is present in the structure or 0 otherwise. The following
animation shows us starting from an empty structure and adding each edge one by one in order, with a
[Schlegel diagram](https://en.wikipedia.org/wiki/Schlegel_diagram) showing the edge numbering. Bits
are numbered from 0 (least significant) to 29 (most significant):

<center>
<video controls="controls" style="outline:none; max-height:40vh; max-width:100%;" autoplay loop muted playsinline>
  <source src="/images/dodecahedra/Stationary_final.mp4">
</video>
</center>

You might notice this particular choice of numbering seems to spiral around
the dodecahedron in groups of 5, e.g. the first five edges go in counterclockwise order around
the bottom-most face. This grouping turns out to be useful for computing rotations.
Consider the following bit manipulation operations:

```rust
const ROT1_MASK_A: u32 = 0b11110_11110_11110_11110_11110_11110;
const ROT1_MASK_B: u32 = 0b00001_00001_00001_00001_00001_00001;

fn rot1(structure: u32) -> u32 {
    return (structure & ROT1_MASK_A) >> 1
         + (structure & ROT1_MASK_B) << 4;
}
```

The first bit mask selects 4 bits from each group of 5 which we shift 1 bit to the right.
The second bit mask selects the remaining bit from each group and shifts them 4 bits to the left.
This effectively cycles each group of 5 bits in a way which resembles rotation. The following
animation visualizes the bit shifts on an arbitrary structure:

<center>
<video controls="controls" style="outline:none; max-height:40vh; max-width:100%;" autoplay loop muted playsinline>
  <source src="/images/dodecahedra/rot1.mp4">
</video>
</center>

As is, this operation is only enough to allow us to cycle through five possible rotations of a
dodecahedron before it begins to repeat positions. In order to get the rest, we'll need to find a way to rotate each structure
around a different axis. Unfortunately I could not find a more elegant way to do the second rotation
other than staring at the diagram and rotating shapes in my head until coming up with
the following mapping of edges from their old positions to their new positions:

```
 0➔ 5  1➔11  2➔16  3➔ 6  4➔ 1
 5➔15  6➔21  7➔12  8➔ 2  9➔ 0
10➔ 9 11➔20 12➔26 13➔17 14➔ 3
15➔10 16➔25 17➔22 18➔ 7 19➔ 4
20➔19 21➔29 22➔27 23➔13 24➔ 8
25➔24 26➔28 27➔23 28➔18 29➔14
```

Unlike our first "clean" rotation, there is no convenient shortcut to shuffle the bits
and instead we must explicitly apply each of the mappings.

```rust
const ROT2_MAP: [u8; 30] = [5, 11, 16, 6, ...];
fn rot2(mut repr: u32) -> u32 {
    let mut result = 0;
    for offset in ROT2_MAP {
        result |= (repr % 2) << offset;
        repr >>= 1;
    }
    return result
}
```

*(Technically you can
squeeze all of this into a handful of CPU cyles with [x86 intrinsics](https://stackoverflow.com/questions/54408726/whats-the-fastest-way-to-perform-an-arbitrary-128-256-512-bit-permutation-using))*

This gives us a second rotation around a new axis:

<center>
<video controls="controls" style="outline:none; max-height:40vh; max-width:100%;" autoplay loop muted playsinline>
  <source src="/images/dodecahedra/rot2.mp4">
</video>
</center>


By applying sequences of these two rotations we can derive any of the 60 total possible rigid
rotations of a dodecahedron (in group theory terms, they form a [generating set](https://en.wikipedia.org/wiki/Generating_set_of_a_group)).
To remove duplicate structures under rotation, we can apply all 60 rotations to
each structure and use the bit representation corresponding to the smallest integer
as the "canonical" representation. If two structures are equivalent under rotation, they should
both yield the same canonical representation. For example, the following diagram shows
all 60 structures with the canonical representation of 63:

<center><img src="/images/dodecahedra/63.png" style="max-height:60vh">
</center>

# Keeping in touch

Now that we have a method to deduplicate structures we can start looking at other conditions.
The next major condition states every edge needs to be connected,
i.e. there shouldn't be any groups of edges which "float" disconnected from the
rest of each structure. One way to check this would be to use a data structure
like a [merge-find set](https://en.wikipedia.org/wiki/Disjoint-set_data_structure). In
practice this can be a bit slow, and would require us to check hundreds of millions of invalid structures.
Instead of checking each possible structure for connectedness, we can
build connected structures "bottom-up" by appending connected edges one-by-one to existing
structures:

<center><a href="https://www.math.ksu.edu/~rozhkovs/LeWitt_cubes.pdf" target="_blank"><img src="/images/dodecahedra/cube-buildup.jpg" style="max-height:60vh"></a>
<br>
<i>
Diagram showing the construction of incomplete open cubes by appending edges one at a time used in <a href="https://www.math.ksu.edu/~rozhkovs/LeWitt_cubes.pdf" target="_blank">"Is&nbsp;the&nbsp;List&nbsp;of&nbsp;Incomplete&nbsp;Open&nbsp;Cubes&nbsp;Complete?"</a>.
</i>
</center>

To do this efficiently, we can once again use bit manipulation tricks on the binary representations
of our structures. We start by finding all pairs of edges connected by a shared vertex and determine
their binary representations:

<center>
<video controls="controls" style="outline:none; max-height:40vh; max-width:100%;" autoplay loop muted playsinline>
  <source src="/images/dodecahedra/3.mp4">
</video>
</center>


We can use these pairs to identify new edges to append to existing structures.
Bitwise `&` gives us the "intersection" of two structures, i.e. any edges which are
in both structures. When `&`'ing an arbitrary structure against our "pair" structures, there
are three possible outcomes:
* Neither of the edges of the pair are in the arbitrary structure. This results in the empty structure represented by 0.
* Exactly one of the edges of the pair is in the arbitrary structure. This results in the one shared edge.
* Both edges of the pair are in the arbitrary structure. This gives us back the original pair structure.

<center><img src="/images/dodecahedra/ampersand.jpg" style="max-height:60vh">
</center>


The second case is useful since it means one of the edges is already part
of the arbitrary structure, while the other edge is not part of the arbitrary structure but *is* connected to
an existing edge. In this case we can bitwise `|` the pair with the arbitrary structure
to add one new connected edge to it:


<center><img src="/images/dodecahedra/or.jpg" style="max-height:21.9vh">
</center>

This gives us a general approach for finding every unique non-empty and connected structure:
* Start with a single edge, i.e. the structure represented by the integer 1.
* Given the canonical forms of all connected structures with N edges, we can construct
the set of canonical forms of all connected structures with N+1 edges by doing the following:
    * For each N edge structure, iterate through every pair structure.
    * If the N edge structure and the pair structure have exactly one edge in common,
      compute the bitwise `|` of the two.
    * Add the canonical form of the `|` structure to the set of N+1 edge structures.
* Continue until you construct the "complete" dodecahedron where all 30 edges are present.

The following diagram shows the steps used to build the canonical forms of all connected
structures up to 5 edges via this approach:

<center><img src="/images/dodecahedra/layers.jpg" style="max-height:75vh">
</center>

# Loose ends

With this, we now have the set of all connected structures deduplicated under rotation.
As a reminder, the original conditions for *Incomplete Open Cubes* were:
* All of the edges are connected.
* At least one edge is missing.
* The structure is 3-dimensional (the edges aren't all part of the same face).
* Each structure is unique, treating rotations as equivalent.

The first and last conditions were both covered by the previous sections. The second and
third can be covered by simply removing the canonical forms of the invalid structures.
The first five are the structures where every edge is part of the same face, while the last is the
"complete" dodecahedra without any edges missing:

<center><img src="/images/dodecahedra/excluded.jpg">
</center>

With those removed we get a final count of 2,423,206 structures:

<center><img src="/images/dodecahedra/chart.png" style="max-height:40vh"></center>

LeWitt's original installation used
one square foot per structure, meaning to replicate it with dodecahedra we would
need 2.4 million square feet, or about 42 football fields of space. This is slightly too large
to fit in my studio apartment, so we'll need to resort to a digital version instead. The following
came to me in a fever dream after watching a certain movie:

<center><a href="/dodecahedra/hallway.html" target="_blank"><img src="/images/dodecahedra/backrooms.jpg" style="max-height:60vh"></a><br>
<i>Click <a href="/dodecahedra/hallway.html" target="_blank">here</a> to explore for yourself!</i>
</center>

Coming back around to the original motivation for this project, the question arises of whether
or not ripping off Sol LeWitt and the backrooms simultaneously should count as art. At the end of the day,
whether or not something qualifies as art is a purely subjective matter, and personally I think there's
something beautiful and thought-provoking about the emergent structure of the incomplete
open dodecahedra which gives it artistic merit. And, as the recipient of a Bachelor of
$${\color{#dd2222}\mathcal{A}}{\color{#dd8800}\mathfrak{r}}{\color{#00aa00}\mathfrak{t}}{\color{#0000ff}\mathfrak{s}}$$,
my subjective opinion on this matter is basically an objective fact. Thanks for reading!


<center>
<img src="/images/dodecahedra/print.jpg" style="max-height:60vh"><br>
<i>3D print of one of my favorite structures, you can interact with it and other structures
<a href="/dodecahedra/viewer.html?value=989814703&outline=0" target="_blank">here</a>.<br> For fun,
try figuring out what kind of symmetry it has!
</i>
</center>

Related topics:
* ["Incomplete Open Platonic Solids"](https://arxiv.org/pdf/2602.20425) by Mikael Vejdemo-Johansson
covers the rest of the Platonic solids. Obviously there's
a lot of overlap with their work and my own, a bit of proof I didn't just plagiarize them
is this [enumeration code](https://github.com/ckw017/dodeca) I uploaded 4 years ago.
* ["Exploration & Epiphany"](https://www.youtube.com/watch?v=_BrFKp-U8GI) by Paul Dancstep. Guest video on 3blue1brown's channel which goes into
further detail exploring the symmetries of *Incomplete Open Cubes* and group theory-esque insights.
* <a href="https://www.math.ksu.edu/~rozhkovs/LeWitt_cubes.pdf" target="_blank">"Is&nbsp;the&nbsp;List&nbsp;of&nbsp;Incomplete&nbsp;Open&nbsp;Cubes&nbsp;Complete?"</a>
(presumably by [Natasha Rozhkovskaya](https://www.math.ksu.edu/~rozhkovs/)). Enumeration of
the original incomplete open cubes problem.
* <a href="https://oeis.org/A222186" target="_blank">OEIS A222186</a> - Online Encyclopedia
of Integer Sequences for this problem in 1 to 4 dimensions. According to this the number of
incomplete open hypercubes comes out to 14632580 (note that this sequence includes the
"complete" structure, so we subtract 1).
* ["Incomplete Open Cubes Revisited"](https://cubes-revisited.art/) by Rob Weychert. Explores
the possible structures if you remove the connectedness requirement.
