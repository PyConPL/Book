Journey to the center of the the asynchronous world
===================================================

Introduction
------------

Since the release of Python 3.4, one of the hottest and most frequently mentioned
topics is the [asyncio](https://docs.python.org/3/library/asyncio.html) module,
introduced in [PEP 3156](http://legacy.python.org/dev/peps/pep-3156/).
In the following short article I'll try to show you some cool stuff that lies
at the core of this module. But before we dig in, there is one warning: most of the
samples presented in this article are written in Python 3.4, so make sure to use
at least that version when running the examples. These can be found at
[my github account](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples).


Generators
----------

Let's start with this sample piece of code,
[generator1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator1.py):

```python
def countdown(n):
    while n > 0:
        yield n
        n =- 1
```

As you've probably noticed, this is one of the simplest generator functions
imaginable. Its typical usage is as following:

```python
for x in countdown(10):
    print("Got ", x)
```

This prints every number starting from 10 down to 1. So we can conclude
that every function written using the `yield` statement is a generator, which
can then be used to feed all kinds of loops and iterations. If we look under
the hood, this iteration calls `next()` to get the next value from the
generator, until it reaches the `StopIteration` exception. We can illustrate that
with the following piece of code:

```python
c = countdown(3)
print(c)
next(c)
next(c)
next(c)
next(c)
```

The result of running this code is:

```
<generator object countdown at 0x7f2b0fa7a0d0>
3
2
1
Traceback (most recent call last):
  File "generator1.py", line 21, in <module>
    print(next(c))
StopIteration
Traceback (most recent call last):
  File "stdin", line 1, in ?
    print(next(c))
StopIteration
```

This is just the beginning, to make sure that everyone is on the same page.
Expect more of the promised awesomeness to come! What is probably a lesser known
fact, is that the `yield` statement can be used to receive values,
[generator2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator2.py):

```python
def receiver():
    while True:
        item = yield
        print("Got: ", item)

c = receiver()
print(c)
next(c)
c.send(43)
c.send([1, 2, 3])
c.send("Hello")
```

The output of the above code is as following:

```
<generator object receiver at 0x7f1690d88f58>
Got:  43
Got:  [1, 2, 3]
Got:  Hello
```

This was introduced in [PEP 342](http://legacy.python.org/dev/peps/pep-0342/),
where the idea of coroutines appeared for the first time. This PEP extends the
functionality of the generators presented in the first example with the possibility
to send values to the generators. Essentially any function having the `yield`
statement in its body is actually a generator. This means that it is not going
to execute, but rather it will return a generator object, which provides the following
operations:
* `next()` - advance code to the `yield` statement and emit a value, if such was
  passed as a parameter. That's the only operation you can call after creating
  the generator.
* `send()` - sends a value to the `yield` statement, making it produce a value instead
  of emitting one. Remember to call `next()` beforehand.
* `close()` - a way to inform the generator that it should finish its work.
  It generates the `GeneartorExit` exception upon calling the `yield` statement.
* `throw()` - gives you the opportunity to send an error to generator upon a call
  to the `yield` statement.

In Python 3.4 specifically you can have both the `yield` and the `return` statement.
In previous Python versions this would be a syntax error. Currently if you write,
[generator3.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator3.py):

```python
def returnyield(x):
    yield x
    return "Hi there"

ry = returnyield(5)
print(ry)
print(next(ry))
print(next(ry))
```

The output of the above code is as following:

```
<generator object returnyield at 0x7f27bf38bf58>
5
Traceback (most recent call last):
  File "generator3.py", line 15, in <module>
    print(next(ry))
StopIteration: Hi there
```

If you carefully study the output, you'll notice that the value of the `return`
statement is actually passed as a value of the `StopIteration` exception.
Interesting, isn't it?


Delegating to a subgenerator
--------------------------

[PEP 380](http://legacy.python.org/dev/peps/pep-0380/) proposed the syntax for a
generator to delegate part, or all, of its work to another generator. This
basically means that instead of manually iterating, we're passing the generation
to somebody else, who will do it for us. This is presented in
[yieldfrom.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/yieldfrom.py):

```python
def yieldfrom(x, y):
    yield from x
    yield from y

x = [1, 2, 3]
y = [4, 5, 6]
for i in yieldfrom(x, y):
     print(i, end=' ')
```

The expected output is a series of numbers from 1 to 6. What is happening here
is that both of these `yield from` statements take values from both lists, consume
them and join them as if they were one list. In its simplest form, these can
be seen as hidden `for` loops, but soon you'll see there's more to it. Beyond this,
there is the concept of generator chaining, meaning iteration can be delegated
even further. Let's create something more complicated:

```python
for i in yieldfrom(yieldfrom(a, b), yieldfrom(b, a)):
    print(i, ' ')
```

In the above example, the outermost call will delegate iteration to the inner
generators until we reach a single value that will be yielded.


Context managers
----------------

Let's leave the generator and coroutines topic for a bit and look at something
different. I'm hoping the reader is familiar with these constructs:

```
file = open()
# do some stuff with file
file.close()

lock.acquire()
# do some stuff with lock
lock.release()
```

These constructs are currently nicely handled by context managers, introduced in
[PEP 343](http://legacy.python.org/dev/peps/pep-0343/) - the `with` statement.
Context managers are basically normal objects implementing two methods:
* `__enter__(self)` - start work with your object, returning it
* `__exit__(self, exc, val, tb)` - release the object, or handle the exception

Let's create a simple context manager for working with a temporary directory,
[contextmanager1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/contextmanager1.py):

```python
class tempdir(object):
    def __enter__(self):
        self.dirname = tempfile.mkdtemp()
        return self.dirname
    def __exit__(self, exc, val, tb):
        shutil.rmtree(self.dirname)

with tempdir() as dirname:
    print(dirname, os.path.isdir(dirname))
```

This sample context manager will create a temporary directory, whose name will be
printed and then checked for it's existence. Thanks to the awesome Python core
developers, the `yield` statement and the `@contextmanager` decorator, the above
code can be rewritten as follows,
[contextmanager2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/contextmanager2.py):

```python
@contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname # the magic happens here
    finally:
        shutil.rmtree(dirname)
```

You will use this piece of code in exactly the same way as in the previous context
manager. The only difference is how you define your context manager. In the latter
example, the decorator is creating the context manager for you, and `yield` returns the
temporary directory. If you look under the covers you'll see that calling
`tempdir()` in the first example will return `<__main__.tempdir object at 0x7f3e4778f5a0>`
whereas the later - `<contextlib._GeneratorContextManager object at 0x7fd94c7ce538>`.
Do you see the difference? If you look closely at the `@contextmanger` decorator
you'll find out that it sets up the `__enter__()` and `__exit__()` methods,
with some additional error checking, see:
[contextlib.py#96](http://hg.python.org/cpython/file/3.4/Lib/contextlib.py#l96).
For those of you concerned about performance, my test shows the decorator
solution runs ~9% slower than its class counterpart, but think of how much easier
to read the decorator solution is.


Asynchronous processing
-----------------------

Finally we've reached the last part - asynchronous processing. The usual way
of processing in such cases is: we have some main thread; in it we run some
asynchronous function, and after some time we reach for the results.
This is a very common programming pattern, which can be presented with the following
code, [future1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/future1.py):

```python
def executor(x, y):
    time.sleep(10)
    return x + y

pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.result()
```

The above code runs in a different thread, but here we're blocked; we wait
until we get the result. The next example shows how to use callback functions
that will return when the result is ready, whereas in the meantime we still have
control over the main thread,
[future2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/future2.py):

```python
def handle_result(result):
    """Handling result from previous function"""
    print("Got: ", result.result())

pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.add_done_callback(handle_result)
```

A quick note: if an exception happens inside the executor method, it will be
returned when getting the result. Testing this will be left as an exercise to
the reader.


`asyncio` basics
----------------

OK, we've reached a point where I've shown you a couple of cool tricks with
generators, but you may be asking "How is this useful? What can we do with it?"
Let's then move to the final part where I'll show you how, using previous parts
we can bypass certain Python limitations and create `asyncio` core functionality.

Let's start with creating a task object, which is similar to what I've shown you
before, but this time, we'll put the idea into a reusable object,
[task1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/task1.py):

```python
class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None):
        try:
            fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        result = fut.result()
        self.step(result)
```

If you look at the code you'll notice it is almost identical to the previous
one, but placed inside of some sort of a context manager class. The only
difference being method names, `step()` in place of `__enter__()` and `_wakeup()`
for `__exit__()`. What we have here, actually, is a task object accepting
a generator as the only initialization parameter, with the main function `step()`
responsible for advancing the generator to the next `yield` statement, sending
in a value and a callback to do something with the result. There's also one
little trick at the end of the attached callback method called `_wakeup()` where we
feed ourselves with the result to proceed execution to the next `yield`
statement.

So let's create a recursive function, to show that using the above tricks we can
bypass Python's recursion limit which by default is
[1000](http://hg.python.org/cpython/file/3.4/Python/ceval.c#l687).

```python
def recursive(pool, n):
    yield pool.submit(time.sleep, 0.001)
    print(n)
    Task(recursive(pool, n+1)).step()
```

If you run it long enough, you'll notice that in using this little trick Python
doesn't have a stack limit any more. What's more, the execution does not provide
any overhead when run. You should definitely check it if you don't believe me.

There's still one more modification to our `Task` object which I'd like to show you.
So far, this class can only process background tasks, but how do you return something
from that background task? Let's use the `concurrent.futures.Future` object as a
base class for our `Task`. To perform this we need to do a little Python patching,
meaning we need to make the `Task` class iterable to be used inside the `yield from`
statement:

```python
def patch_future(cls):
    def __iter__(self):
        if not self.done():
            yield self
        return self.result()
    cls.__iter__ = __iter__
```

Then we can properly modify our `Task` object to return the result:

```python
class Task(Future):                     # <--

    def __init__(self, gen):
        super().__init__()              # <--
        self._gen = gen

    def step(self, value=None):
        try:
            ...
        except StopIteration as exc:
            self.set_result(exc.value)  # <--
```

Now we can use the `Task` object to do some intensive calculation and retrieve
the result, [task2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/task2.py).

```python
def calc(x, y):
    print("I'm going to sleep for a while...")
    time.sleep(10)
    return x + y

def do_calc(pool, x, y):
    result = yield from pool.submit(calc, x, y)
    return result

if __name__ == '__main__':
    pool = ProcessPoolExecutor(8)
    t = Task(do_calc(pool, 2, 3))
    t.step()
    print("Got ", t.result())
```

Summary
-------

The attentive reader might say at this point, "We're at the summary already, but
you've promised to show what `asyncio` internals look like!" But I just did that:
the last example of the `Task` object is almost exactly the same as the one in
the `asyncio` module. For reference see
[tasks.py#25](http://hg.python.org/cpython/file/3.4/Lib/asyncio/tasks.py#l25),
with more error handling, and most importantly, some additional useful functions
which hide implementation details from users to make it easier to use. Of
course, there's also the most important thing, which is the event loop being the
core runner instead of thread pools.

Hopefully, this article made you eager to get more from generators. I highly
recommend reading David Beazley's trilogy on this topic:

1. [Generator Tricks for Systems Programmers](http://www.dabeaz.com/generators/)
2. [A Curious Course on Coroutines and Concurrency](http://www.dabeaz.com/coroutines/)
3. [Generators: The Final Frontier](http://www.dabeaz.com/finalgenerator/)

I also would like to thank him for giving me the chance to use his materials as
an input for my article and presentation. Additionally, check out his awesome,
mind-blowing book [Python Cookbook](http://shop.oreilly.com/product/0636920027072.do).
