---
layout: post
img: /images/blursed.png
title: Blursing Python
---

*"**blursed** (adj): Simultaneously blessed and cursed by a situation, object, person, etc..."* 

-- [Urban Dictionary](https://www.urbandictionary.com/define.php?term=Blursed)

I recently discovered something incredibly blursed while reading an article by `faehnrick` in [PagedOut](https://pagedout.institute/) Volume 2. In an article titled "Abusing C - Have Fun!" on the topic of obsfuscated C code it's demonstrated that this sort of thing is valid C:

```c
#include <stdio.h>

int main() {
    for(int i = 0; i < 12; i++)
        printf("%c", i["Hello World!"]);
    printf("\n");
}
```

The interesting bit inside the for loop, where it appears we're indexing *into* an `int` *with* a c-string. Intuitively this doesn't make any sense, so maybe it's just one of the infinite number of things in C that can compile but will just result in garbage. Checking the output we get:

`Hello World!`

Ah, yup garba -- wait what? What happened here? The key is to realize that brackets are really just syntactic sugar in the sense that each of the following prints are equivalent:

```c
char* s = "abcd";
printf("%s\n", s[2]); // Normal usage
printf("%s\n", *(s + 2)); // Without the syntactic sugar
printf("%s\n", *(2 + s)); // Commute!
printf("%s\n", 2[s]); // Oh no
```

So that's C, but this article is about blursing Python. Surely Python wouldn't let something like this fly, right?

```python
>>> print(0["Blursed?"])
<stdin>:1: SyntaxWarning: 'int' object is not subscriptable;
perhaps you missed a comma?
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not subscriptable
```

*Apparently Python 3.8 gives firendly little advice now :O*

And as expected errors as `int` objects aren't allowed to be indexed into. Unless...?

The way Python decides whether or not you can index (or subscript, as the error message uses) into something is if the class has a `__getitem__` method. You may recognize this as a "dunder" method, which is how Python implements operator overloading. More on that [here](https://www.geeksforgeeks.org/dunder-magic-methods-python). So, hypothetically, if we implemented this function for the int class we could get the behavior we wanted, right?

```python
>>> def getitem(self, other):
...     return other[self]
... 
>>> int.__getitem__ = getitem
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't set attributes of built-in/extension type 'int'
```

Well shoot, it looks like we aren't allowed to assign any attributes into built-in types (int, float, complex, bool, etc...). So we're stuck, right? This is where I'll admit that I didn't go out of my way to introduce this abomination of a "feature" into Python. As a matter of fact, the method comes from a separate attempt to introduce a different, slightly less abominable feature into Python.

Let's open a new stack frame for this... 

---

## Frame 1: A slightly less abominable use case

Python is my go to tool for doing calculations because of its builtin implementation of big integers. Last semester I took [CS188 (Intro to AI)](https://inst.eecs.berkeley.edu/~cs188/) which loved more than anything to give assignments that made you *be* a rational agent, i.e. chugging through hand calculations of cost and reward functions. Needless to say I trust the Python interpreter to do calculations more correctly than I ever could. Sadly I ran into a problem almost non-stop:

```python
>>> 188(123 + 456)
```

Since most of the time I was just copying in whatever I had written in my notes down verbatim I ended up keeping the traditional "2(1 + 1) = 2 * (1 + 1)" syntax of normal arithmetic. Python of course expects the asterisk to be there to indicate multiplication, so we get:

```python
<stdin>:1: SyntaxWarning: 'int' object is not callable;
perhaps you missed a comma?
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not callable
```

But wait, this looks familiar doesn't it? The first time the interpreter was peeved because we were subscripting an int, and here it's peeved that we're trying to call it. After all "188(...)" to the interpreter just looks like we're trying to "call" the constant 188 as a function. So we still have the same problem before. So how to get around this?

Earlier the main problem was that we can't assign new attributes to built-in types. But what about subclasses of built-in types? For example, this totally works:

```python
class callable_int(int):
    def __call__(self, other):
        return self*other

print(callable_int(186)(123 + 456))
```

*Output: 107694*

Of course casting every integer (or numeric type in general) is quite a mouthful. If only there were a way to somehow *modify the file before running it to slip in these casts implicitly*.

Let's open a new stack frame for this...

---

## Frame 2: Future Fstrings

Fstrings are a feature introduced in Python 3.6 that lets you do this:

```python
location = "Dresden"
print(f"Hello {location}!")
```

*Output: Hello Dresden!*

This isn't backwards compatible with earlier versions of Python:

```python
Python 3.5.6 |Anaconda, Inc.| (default, Aug 26 2018, 21:41:56) 
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> location = "Xanadu"
>>> print(f"Hello {location}!")
  File "<stdin>", line 1
    print(f"Hello {location}!")
                             ^
SyntaxError: invalid syntax
```

Which makes sense, even if earlier versions could let the `f` prefix to strings slide, they would have no idea how to interpret the format notation. And yet, it seems that there's a package which allows this kind of compatability. The package [future-fstring](https://github.com/asottile/future-fstrings) allows for older versions of python to use fstrings. After installing you can run this file as expcted:

```python
# -*- coding: future_fstrings -*

location = "Ithaca"
print("Hello {location}!")
```

*Output: Hello Ithaca!*

What's going on here? Let's briefly dive into a new topic:

---

## Frame 3: Codecs

`codec` is short for **co**der **dec**oder. Codecs crop up a lot in audio and video streams to compress information by encoding it on the senders end and decoding it on the receivers end, overall decreasing the network cost. In Python codecs are used to interpret the text passed into the script. You may have encountered this before when working with python2, which by default uses the ascii encoding. So something like this will happen by default:

```python
>>> gödel = True is False
  File "<stdin>", line 1
    gödel = True is False
     ^
SyntaxError: invalid syntax
```

You may have noticed that for compatibility with python3, which uses utf-8 by default, Python files will occasionally lead off like this:

```python
# -*- coding: utf8 -*
gödel = True is False
```

Python will read off the codec specified and use it to decode the file from raw bytes into the tokens that will ultimately end up in the AST. 

We can pop out of the topic of codecs now

## Frame 3: End

---

Back to frame 2, on future_fstrings.

So how does this tie in with future_fstrings? It turns out that future_fstring just adds a new codec that decodes as utf8 would, and then modifies the result before returning:

In: [future_fstrings.py](https://github.com/asottile/future-fstrings/blob/master/future_fstrings.py)

```python
def decode(b, errors='strict'):
    import tokenize_rt # Tokenizer

    u, length = utf_8.decode(b, errors) # Use regular utf8 codec to decode
    tokens = tokenize_rt.src_to_tokens(u) # Tokenize the result
    ...
    # Modify tokens
    ...
    return tokenize_rt.tokens_to_src(tokens), length # Return modified tokens as src
```

After passing this codec over the raw source, this:

```python
# -*- coding: future_fstrings -*-
thing = 'world'
print(f'hello {thing}')
```

Is seen by the interpreter as:

```python
# -*- coding: future_fstrings -*-
thing = 'world'
print('hello {}'.format((thing)))
```

Okay, we can pop out of frame 2 now.

## Frame 2: End

---

Back to frame 1, where we're trying to find a way to slip in casts to `callable_int` around regular `int`. Well, using the technique from future_fstrings this can be accomplished fairly easily. With a new encoding we can do:

```python
def decode(b, errors='strict'):
    u, length = utf_8.decode(b, errors)
    tokens = tokenize_rt.src_to_tokens(u)
    new_tokens = []
    for token in tokens:
        if token.name == 'NUMBER': # Wrap any tokens that look like numeric literals
            new_tokens.extend(
                tokenize_rt.src_to_tokens(
                    "callable_int({})".format(token.src)
            ))
        else:
            new_tokens.append(token)
    return tokenize_rt.tokens_to_src(new_tokens), length
```

After installing the new codec:

```python
# -*- coding: callable_numerics -*-
186(123 + 456)
```

Is passed to the interpreter as

```python
# -*- coding: callable_ints -*-
callable_int(186)(callable_int(123) + callable_int(456))
```

Which is evaluated as 107694 without complaint! Time to pop one last time:

## Frame 1: End

---

Back to frame 0! This whole frame business is a play on call stacks, which I've found have sometimes been an apt metaphor for discussions that end up having to nest deeper and deeper into "moderately related tangents" and slowly get resolved outwards into the original topic. And we're finally back to our original goal: blursing Python!

Well, at this point it should be fairly straightforward to blurse python. We adjust callable_int with a new dunder method:

```python
class blursedint(int):
    def __getitem__(self, other):
        return other[self]

    def __call__(self, other):
        return self*other
```

Once we modify the codec we can get the behavior we want!

Of course there are some caveats that implementation wise aren't as interesting to talk about, however are present in the source including a not limited to:
* Blursing the other numeric types in python, `complex` and `float`
* Making blurses "contagious", i.e. 123(456)(789) should still be valid! So 123*456 should also be blursed
* Lots and lots of decorators... Which I've found have plenty of [(ab)use cases](/Decorators)!
* An **extra** blursed implementation of float

The final result runs the following file:

```python
# -*- coding: blursed -*-

print("Multiplications")
print(1.5(24 + 12 + 1)(238 * 3)(512))
print(16(12 * 12) + 512)

print("\nIndexing")
sup = "Konichiwhat's up"

print(7[sup])
print(8[sup])
print(9[sup])
print(10[sup])

ohno = [0,1,2,3,4]

print("\nFloat indexing")
print(2.7[ohno])
print(0.5[ohno])

why = [0,5,31,12]

print(1.5[why])

```

Outputing this (try to guess what's going on with float indexing!):

```
Multiplications
20289024.0
2816

Indexing
w
h
a
t

Float indexing
2.7
0.5
18.0
```

Hopefully you now have a good idea of what I mean when I say blursed! The source for this can be found [here](https://github.com/ckw017/blursed). If you want to experience this travesty firsthand, Python 3.5+ should be able to take use this properly after running `pip install blursed`. And as always, thanks for reading.