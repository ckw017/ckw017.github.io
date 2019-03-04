---
layout: post
img: https://i.imgur.com/uKBTjsf.png
title: "Python Decorators: Not just for decoration"
---

Python decorators are the semantic sugar that most people will
run into while working with web frameworks such as Flask or Bottle. 
For example, the following snippet from the Bottle documentation uses
decorators to specify a route:

```python
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

#Equivalent to index = route('/hello/<name>')(index)
```

In fact the most common use of decorators is to allow framework users 
to hook into some interesting functionality. Of course, there 
are some uses in more common cases. Consider the following decorator:

```python
def memoize(f):
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized
```

``memoize`` is a higher order function that takes ``f`` (another function) as
input. It creates a dictionary ``cache``, then returns the function ``memoized``. Upon closer inspection, ``memoized`` checks whether ``cache`` already contains
its arguments. If not, it computes the value of ``cache[args]`` with ``f``.

This function is incredibly useful for recursive routines without side-effects.
For example, consider the textbook example of "there's a time and place for 
recursion, but not now!":

```python
def fib(n):
    if n <= 1:
        return 1
    return fib(n - 1) + fib(n - 2)
```

This function would normally sport an elegantly inefficient 2^n runtime.
However, applying the memoize decorator would cache the result of each call
to ``fib(n)`` for n in [0..n-1]. This caching procedure reduces the runtime from
exponential to linear (at the cost of memory). 

*A pragmatist would argue to solve the problem iteratively (and a 
hyper-pragmatist would suggest exploiting matrix multiplies), but in such
a case I wouldn't have an excuse to use decorators.*

This however, is just the surface of decorators. Back to the framework
examples, I recently put together a [python module for writing Pokemon Showdown chat clients](https://github.com/ckw017/showdown.py/) (you can read about why I've done so [here](/Rock-Paper-Scissors/)). One of the challenges of writing
a module for other's people use is the necessity for consistent documentation.
Consider the following two function docstrings (apologies in advance for asking you to read documentation):

```python
def private_message(self, user_name, content, strict=False)
    """
    Sends a private message with content to the user specified by user_name.
    The client must be logged in for this to work.

    Params:
        user_name (:obj:`str`) : The name of the user the client will send 
            the message to.
        content (:obj:`str`) : The content of the message.
        strict (:obj:`bool`, optional) : If this flag is set, passing in 
            content more than 300 characters will raise an error. Otherwise,
            the message will be senttruncated with a warning. This paramater
            defaults to False.

    Notes:
        Content should be less than 300 characters long. Longer messages 
        will be concatenated. If the strict flag is set, an error will be 
        raised instead.
    """

def say(self, room_id, content, strict=False)
    """
    Sends a chat message to the room specified by room_id. The client must
    be logged in for this to work

    Params:
        room_id (:obj:`str`) : The id of the room the client will send the 
            message to.
        content (:obj:`str`) : The content of the message.
        strict (:obj:`bool`, optional) : If this flag is set, passing in 
            content more than 300 characters will raise an error. Otherwise,
            the message will be sent truncated with a warning. This 
            paramater defaults to False.

    Notes:
        Content should be less than 300 characters long. Longer messages 
        will be concatenated. If the strict flag is set, an error will be
        raised instead.

    """
```

There's something wrong here. Very, very wrong. Can you spot it? That's right,
we're repeating ourselves all over the place! The two functions involved, 
``private_message`` and ``say`` both do essentially the same thing: send a
message somewhere. As such, their parameters and docstrings bear nearly
identical content, in two different parts of the code base. This violates a
basic rule of programming best practice: **D**on't **R**epeat **Y**ourself.
The problem lies in trying to update individual parts of the docstring. What
if at some point I chose to concatenate messages at the 350 character limit? I
would have to update the "Notes:" entry of the docstrings in two different
places. This shall not stand.

As you may have guessed from the previous article content, the solution here is
decorators! If you take a look at the source code for ``showdown.client``, the
actual function declarations look like this:

```python
@docutils.format()
async def say(self, room_id, content, strict=False):
    """
    Sends a chat message to the room specified by room_id. The client must
    be logged in for this to work

    Params:
        {room_id}
        {content}
        {strict}

    Notes:
        {strict_notes}
    """
```

What's going on here? I will take this moment to comment on the fact that the 
Python language allows users to do some deep, dark acts of programmatic black
magic. The answer to any question of the form "Hey, can I do {unspeakable act usually involving self-modifying code} in python?" is "Yes, however ``PEP 666 + 2/3`` recommends that you reread Goethe's *Faust* before proceeding." The 
 feature
used here barely qualifies as one of such acts, but might be classified as a
first step towards future acts of Lovecraftian nature.

To be less dramatic, you can modify docstrings (and function signatures for
that matter) programmatically, so that they display differently when calling
``help()`` in the interpreter. We can use decorators here to do away with
some of the repetition:

```python
#in docutils.py
def format(indent=3):
    full_indent = indent * '    '
    partial_indent = (indent - 1) * '    '
    docstrings = {
        k:v.format(indent=full_indent) for k,v in base_docstrings.items()
    } # base_docstrings is a dict of prewritten docstrings
    def wrapper(func):
        func.__doc__ = func.__doc__.format(**docstrings)
        return func
return wrapper
```

There are a few important details in this snippet. First of all, ``format`` is
a function that returns a function, ``wrapper``, which in turn returns another
function (namely, the modified ``func``). Functions returning function-valued
functions! Welcome to the world of decorators. The outermost function ``format`` is necessary to deal with quirks of indentation in multiline strings. The
inner function modifies the dunder attribute ``__doc__`` and formats in 
appropriate substitutions for ``room_id``, ``content``, etc... as seen in
the previous example. And there we have it! We can modify the part of the
docstring in one place (the entry for ``strict_notes`` in ``base_docstrings``)
and it will update everywhere it is mentioned in the docstrings.

*An extra astute reader might observe that we could automate the process
further by automatically reading the parameters from the function signature
and dynamically generating the "Params:" section of the docstring. While I
considered this, there were various cases within the project where paramater 
name collisions would complicate things, so I chose to forgo it.*

Whether you're writing a framework or using one, decorators are definitely a
handy tool to have in your metaphorical toolbox!