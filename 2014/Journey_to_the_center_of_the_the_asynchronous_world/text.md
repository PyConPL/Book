Journey to the center of the the asynchronous world
===================================================

Introduction
------------

One of the hottest topics, most frequently mentioned since python3.4 was
introduced is [asyncio](https://docs.python.org/3/library/asyncio.html) module,
introduced in [PEP 3156](http://legacy.python.org/dev/peps/pep-3156/).
In the following short article I'll try to show you some cool stuff that lies
at the core of this module. But before we dig in, one warning, most of the
samples presented in this article are written in python3.4, so make sure to use
at least that version when running examples which are available at
[my github account](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples).


Generators
----------

Let's start with this sample piece of code
[generator1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator1.py):

```python
def countdown(n):
    while n > 0:
        yield n
        n =- 1
```

As you've probably noticed this is the simplest generator function you
can think of. It's typical usage is as following:

```python
for x in countdown(10):
    print("Got ", x)
```

This prints every number starting from 10 down to 1. So we can conclude
that every function written using `yield` statement is a generator, which
can than be used to feed all kinds of loops and iterations. If we look under
the cover, this iteration calls `next()` to get the next value from the
generator, until it reaches `StopIteration` exception. We can illustrate that
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

This is of course just the beginning, to make sure everybody will reach the
same level of knowledge. So expect more of the promised awesomeness to come.
What's probably lesser known fact, is that `yield` statement can be used to
receive values,
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

Output of this code is following:

```
<generator object receiver at 0x7f1690d88f58>
Got:  43
Got:  [1, 2, 3]
Got:  Hello
```

This was introduced in [PEP 342](http://legacy.python.org/dev/peps/pep-0342/),
where the idea of coroutines was introduced. This PEP extended the functionality
of generators presented in the first example with possibility to send values
to the generators. So basically any function having `yield` statement in it's
body is actually a generator. Meaning it's not gonna to execute, instead it'll
return a generator object, which provides the following operations:
* `next()` - advance code to `yield` statement and emit value, if such was
  passed as a parameter. That's the *only* operation you can call after
  creating the generator.
* `send()` - sends value to `yield` statement making it produce value instead
  of emitting. Remember to call `next()` beforehand.
* `close()` - closing generator is a way to inform it that it should finish
  his work. It generates `GeneartorExit` exception upon calling `yield`
  statement.
* `throw()` - gives you the opportunity to send an error to generator upon call
  to `yield` statement.

In Python 3.4 specifically you can have both `yield` and `return` statement,
in previous python versions that was syntax error. Currently if you write,
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

Output of above code is following:

```
<generator object returnyield at 0x7f27bf38bf58>
5
Traceback (most recent call last):
  File "generator3.py", line 15, in <module>
    print(next(ry))
StopIteration: Hi there
```

If you carefully study the output you'll notice that the value of the `return`
statement was actually passed as value of the `StopIteration` exception.
Interesting isn't it?


Delegating to subgenerator
--------------------------

[PEP 380](http://legacy.python.org/dev/peps/pep-0380/) proposed the syntax for a
generator to delegate part, or all, of its work to another generator. This
basically means that instead of manually iterating, we're passing the generation
to somebody else, who will do it for us, as presented in
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

Expected output is series of numbers starting from 1 until 6. What happened here
is that both these `yield from` statements took values from both lists, consume
them and spit them as if they were one list. So in it's simplest form, these can
be seen as hidden for loops, but soon you'll see there's more to it. What else
can be done from here is generator chaining, meaning iteration can be delegated
even further. Let's create something more complicated:

```python
for i in yieldfrom(yieldfrom(a, b), yieldfrom(b, a)):
    print(i, ' ')
```

What this piece of code will do is, the outer most call will delegate iteration
to the inner generators and further down until we reach single value that will
be yielded.


Context managers
----------------

For some time we leave the generator and coroutines topic and look at something
different. I'm hoping the reader is familiar with these constructs:

```
file = open()
# do some stuff with f
file.close()

lock.acquire()
# do some stuff with lock
lock.release()
```

These constructs are currently nicely handled by context managers, introduced in
[PEP 343](http://legacy.python.org/dev/peps/pep-0343/) - `with` statement.
Context managers are basically normal objects implementing two methods:
* `__enter__(self)` - start work with your object, returning it
* `__exit__(self, exc, val, tb)` - release the object, or handle the exception

Let's create a simple context manager for working with temporary directory,
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

This sample context manager will create a temporary directory, which name we
print and then check for it's existence. Thanks to awesome python core
developers, `yield` and `@contextmanager` decorator the above code can be
rewritten as follows,
[contextmanager2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/contextmanager2.py):

```python
@contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname # here the magic happens
    finally:
        shutil.rmtree(dirname)
```

You will use this piece of code exactly the same way as previous context manager.
The only difference is how you define your context manager. In the later example
the decorator is creating the context manager for you, and `yield` returns the
temporary directory. If you look under the cover you'll see that calling
`tempdir()` in the first example will return `<__main__.tempdir object at 0x7f3e4778f5a0>`
whereas the later - `<contextlib._GeneratorContextManager object at 0x7fd94c7ce538>`.
Do you see the difference? If you look under the cover of `@contextmanger`
decorator you'll find out that what it does, it sets up the `__enter__()` and
`__exit__()` methods, with some additional error checking, for you, see
[contextlib.py#96](http://hg.python.org/cpython/file/3.4/Lib/contextlib.py#l96).
For those of you concerned about performance, my test shows the decorator
solution runs ~9% slower than it's class counterpart, but think of how much the
decorator solution is easier to read.


Asynchronous processing
-----------------------

Finally we've reached the last part - asynchronous processing. The usual way
of processing in those cases is: we have some main thread, in it we run some
asynchronous function, and after some time we reach for the results.
This very common programming pattern can be presented with the following code,
[future1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/future1.py):

```python
def executor(x, y):
    time.sleep(10)
    return x + y

pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.result()
```

Above code basically runs in a different thread, but here we're blocked, we wait
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

Quick note, if exception will happen inside the executor method it will be
returned when getting the result. Testing this will be left as an exercise to
the reader.


`asyncio` basics
----------------

OK, we've reached a point where I've showed you a couple of cool tricks with
generators, but you may ask how it's useful? What can we do about it? Let's than
move to the final part where I'll show you how using previous parts we can
bypass certain python limitations and create `asyncio` core functionality.

Let's start with creating a task object, which is basically what I've showed you
just before, but this time, we'll put the idea into a reusable object,
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
for `__exit__()`. What we have here actually, is a task object accepting
generator as the only initialization parameter, with main function `step()`
responsible for advancing the generator to the next `yield` statement, sending
in a value and a callback to do something with the result. There's also one
little trick at the end of attached callback method called `_wakup()` where we
feed ourselves with the result to proceed execution to the next `yield`
statement.

So let's create a recursive function, to show that using above tricks we can
bypass python's recursion limit which by default is
[1000](http://hg.python.org/cpython/file/3.4/Python/ceval.c#l687).

```python
def recursive(pool, n):
    yield pool.submit(time.sleep, 0.001)
    print(n)
    Task(recursive(pool, n+1)).step()
```

If you run it long enough, you'll notice that using this little trick python
doesn't have any more stack limit. What's more, the execution does not provide
any overhead when run. You should definiately check it if you don't believe me.

There's still one more modification to our `Task` object I'd like to show you.
So far this class can only process background tasks, but how to return something
from that background task? Let's use `concurrent.futures.Future` object as a
base class for our `Task`. To do it we need to do little python patching,
meaning we need to make `Task` class to be iterable to be used inside `yield from`
statement:

```python
def patch_future(cls):
    def __iter__(self):
        if not self.done():
            yield self
        return self.result()
    cls.__iter__ = __iter__
```

And than we can properly modify our `Task` object to return the result:

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

No we can use the `Task` object to do some intensive calculation and then
retrieve the result, [task2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/task2.py).

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

Careful reader might say, it is summary already but you've promised to show how
`asyncio` internals look like. But I just did that, the last example of the `Task`
object is almost exactly the same as the one in `asyncio` module, see
[tasks.py#25](http://hg.python.org/cpython/file/3.4/Lib/asyncio/tasks.py#l25),
with more error handling and most importantly some additional useful function
that hide implementation details from users to make it easier to use. And of
course there's also the most important thing which is the event loop being the
core runner instead of thread pools.

Hopefully this article made you eager to get more from generators. If so I
highly recommend reading David Beazley's trilogy one this topic:

1. [Generator Tricks for Systems Programmers](http://www.dabeaz.com/generators/)
2. [A Curious Course on Coroutines and Concurrency](http://www.dabeaz.com/coroutines/)
3. [Generators: The Final Frontier](http://www.dabeaz.com/finalgenerator/)

I also would like to thank him for giving me the chance to use his materials as
an input for my article and presentation. So definitely you should check that
out as well as his awesome mind-blowing book
[Python Cookbook](http://shop.oreilly.com/product/0636920027072.do).
