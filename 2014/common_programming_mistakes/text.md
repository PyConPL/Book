# Common programming mistakes in Python
## Dariusz Śmigiel

### Introduction
Python is known as one of the simplest programming languages. You need to know syntax, some basic things like intendation and voilà! You're a developer! But... not so fast. Often it turns out that that's not everything that you need to know about Python to be an efficient developer. You need to know some subtle things. Without this, you can have big problems, because behaviour that you have, is different than expected.

#### Full disclosure
Idea for this talk was taken from work done by Martin Chikilian, originally published at [www.toptal.com/python/top-10-mistakes-that-python-programmers-make][1]

### Mistake #1: Expressions as defaults for function arguments
Python allows to specify default values for function arguments. When function is called without the argument, argument will have assigned value provided as default.
It's a big advantage, because user doesn't have to remember, or even know, about providing values to function. It works pretty good, as long, as you won't give any mutable values there.

    >>> def foo(bar=[]):
    ...     bar.append("baz")
    ...     return bar

#### Current behaviour
It's simple function, where we want to append simple string to list. Expected behaviour of this function, would be:

* create list called `bar`
* append to it a string `baz`
* return list

Unfortunately, it doesn't work like expected. When function is called, we're receiving the same list, with growing number of strings.

    >>> foo()
    ['baz']
    >>> foo()
    ['baz', 'baz']
    >>> foo()
    ['baz', 'baz', 'baz']

#### What's happening?
List `bar` is initialized only once; when function definition is evaluated. That's why, when we're calling `foo`, every time we're appending new string to the same list.
This behaviour is implemented on purpose. [Early binding][2] means that the compiler is able to directly associate the identifier name (such as a function or variable name) with a machine address.

#### Solution

    >>> def foo(bar=None):
    ...     if bar is None:
    ...         bar = []
    ...     bar.append("baz")
    ...     return bar

    >>> foo()
    ['baz']
    >>> foo()
    ['baz']

### Mistake #2: Binding variables in closures
This time, we'll look at [late bindings][3]. Assume, we have function to build 5 next multipliers of given value.

    >>> def create_multipliers():
    ...     return [lambda x : i * x for i in range(5)]
    >>> for multiplier in create_multipliers():
    ...     print(multiplier(2))
    ...

#### Current behaviour
We're expecting to retrieve:

    0
    2
    4
    6
    8

But, instead of this we've got:

    8
    8
    8
    8
    8

#### What's happening?
Closures are *late binding*. The values of variables used in closures are looked up at the time the inner function is called. Whenever any of the returned functions are called, the value of `i` is looked up in the surrounding scope at call time. By then, the loop has completed and `i` is left with its final value of 4. And, contrary to popular belief, it has nothing to do with *lambdas*.

    >>> def create_multipliers():
    ...     multipliers = []
    ...
    ...     for i in range(5):
    ...         def multiplier(x):
    ...             return i * x
    ...         multipliers.append(multiplier)
    ...     return multipliers
    ...
    >>> for multiplier in create_multipliers():
    ...     print(multiplier(2))
    ...
    ...
    8
    8
    8
    8
    8
    >>>

#### Solution
As mentioned in #1, Python evaluates early the default arguments of a function, so we can create a closure that binds immediately to its argumets by using default arg:

    >>> def create_multipliers():
    ...     return [lambda x, i=i : i * x for i in range(5)]
    ...
    >>> for multiplier in create_multipliers():
    ...     print (multiplier(2))
    ...
    ...
    0
    2
    4
    6
    8
    >>>

But, even better idea is change it to explicit:

    >>> def get_func(i):
    ...     return lambda x: i * x
    ...
    >>> def create_multipliers():
    ...     return [get_func(i) for i in range(5)]
    ...
    >>> for multiplier in create_multipliers():
    ...     print (multiplier(2))
    ...
    ...
    0
    2
    4
    6
    8
    >>>

### Mistake #3: Local names are detected statically
Again, our main concern is about [closures][10]. We want to print global `x`, and later change it to new value.

    >>> x = 99
    >>> def func():
    ...     print(x)
    ...     x = 88
    ...

#### Current behaviour
And, again. Something goes wrong.

    >>> func()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "<input>", line 2, in func
    UnboundLocalError: local variable 'x' referenced before assignment

#### What's happening
While parsing this code, Python sees the assignment to `x` and decides that `x` will be a local variable in the function. But later, when the function is actually run, the assignment hasn't yet happened when the print executes, so Python raises an undefined name error.

#### Solution
In this case, we have two solutions: nasty (`global`) and better (reference it through enclosing module name)

    >>> x = 99
    >>> def func():
    ...     global x
    ...     print(x)
    ...     x = 88
    ...
    >>> func()
    99

### Mistake #4: Class variables
We have three classes:

    >>> class A(object):
    ...	    x = 1
    ...
    >>> class B(A):
    ...	    pass
    ...
    >>> class C(A):
    ...	    pass
    ...

#### Current behaviour
After initialization, we're able to get `x` from all classes

    >>> print(A.x, B.x, C.x)
    1 1 1

We can also assign variables:

    >>> B.x = 2
    >>> print(A.x, B.x, C.x)
    1 2 1

And another time:

    >>> A.x = 3
    >>> print(A.x, B.x, C.x)
    3 2 3

Oops.

#### What's happening?
[MRO][4] is happening. Because `C` class has no attribute `x`, it goes to class `A` and returns value for it.

### Mistake #5: Exception handling
Python has nice feature to catch any raised exception. It allows you to prevent the software from crashing, reacting for expected or non-expected situations. In this case, we're using `try/except` clause:

    >>> try:
    ...     list_ = ['a', 'b']
    ...     int(list_[2])
    ... except ValueError, IndexError:
    ...     pass

#### Current behaviour
Our code seems to be very well protected. In one place we're catching value conversion problem and also index bigger than list.
Unfortunately, it doesn't work like we would like to:

    ...
    Traceback (most recent call last):
      File "<input>", line 3, in <module>
    IndexError: list index out of range


#### What's happening?
In Python 2 [old syntax is still supported for backwards compatibility][5]. In modern Python, we would write: `except ValueError as e` what is equal to `except ValueError, e`
In our case, `except ValueError, IndexError` is equivalent to `except ValueError as IndexError` which is not what we want.

#### Solution
Python 3 has no problems with above code. It throws an error, and shows exact place, where something doesn't work:

    File "<stdin>", line 4
      except ValueError, IndexError:

But if you're still using Python 2 and don't see any warning signs, you'll need to follow below solution:

    >>> try:
    ...     list_ = ['a', 'b']
    ...     int(list_[2])
    ... except (ValueError, IndexError) as e:
    ...     pass

Works OK, for both, Python 2 and Python 3.

### Mistake #6: Scope rules
Sometimes, we want to know, how many times some code was run. It would be good, to count it. So, we'll write a simple snippet:

    >>> bar = 0
    >>> def foo():
    ...    bar += 1
    ...    print(bar)
    ...

#### Current behaviour
And run it:

    >>> foo()
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "<input>", line 2, in foo
    UnboundLocalError: local variable 'bar' referenced before assignment

BAM!
The same happens, when we change line `i += 1` to `i = i + 1` It doesn't matter which one is used, both throw an error.

#### What's happening?
Python scope resolution is based on LEGB:

* Local - names assigned in any way within a function (*def* or *lambda*) and not declared global in that function;
* Enclosing function locals - name in the local scope of any and all enclosing (*def* or *lambda*), from inner to outer;
* Global (module) - names assigned at the top-level of a module file, or declared global in a *def* within the file;
* Built-in (Python) - names preassigned in a built-in names module: *open*, *range*, *SyntaxError*, ...

So, when you make an assignment to variable, Python considers it as in local scope. It shadows everything, that is outside this scope. In this case, we don't *see* variable `i` declared before function definition.

#### Solution
Variable needs to be modified in the scope that it was declared in. We can achieve this by passing it as an argument to a function that will return it's new value.

    >>> bar = 0
    >>> def foo(bar=bar):
    ...     bar += 1
    ...     return bar
    ...
    >>> foo()
    1
    >>> foo()
    1

### Mistake #7: Modifying list while iterating over it
Often we need to do something with lists. For instance, remove all odd values from list.

    >>> odd = lambda x: bool(x % 2)
    >>> numbers = list(range(10))
    >>> for i in range(len(numbers)):
    ...     if odd(numbers[i]):
    ...         del numbers[i]
    ...
    Traceback (most recent call last):
	      File "<stdin>", line 2, in <module>
    IndexError: list index out of range

#### What's happening
We're iterating over this list, and when value is odd, we're removing it from list. In the same time list is shrinking, so after few iterations, list is shorter than expected.

#### Solution
Suggested solution, probably the simplest one.

    >>> odd = lambda x: bool(x % 2)
    >>> numbers = list(range(10))
    >>> for n in numbers:
    ...     if odd(n):
    ...         numbers.remove(n)
    ...
    >>> numbers
    [0, 2, 4, 6, 8]

But, we cannot fall into false impression, that this works.

    >>> odd = lambda x: bool(x % 2)
    >>> numbers
    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
    >>> for n in numbers:
    ...     if odd(n):
    ...         numbers.remove(n)
    ...
    >>> numbers
    [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9]

As you may see, it iterates, removes, but also leaves odd numbers.
Does it mean, there is no proper solution for it? No! To solve it, we will use [list comprehensions][6]

    >>> odd = lambda x: bool(x % 2)
    >>> numbers = list(range(10))
    >>> numbers = [n for n in numbers if not odd(n)]
    >>> numbers
    [0, 2, 4, 6, 8]

### Mistake #8: Name clashing with Python Standard Library modules
Sometimes, we forget about simple things. Not every possible module name should be used. Assume, you're creating an application for sending emails.

    app
    |-sender.py
    |-receiver.py
    |-email.py

`sender.py`

    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = 'from@email.com'
    msg['To'] = 'to@email.com'

#### Current behaviour
When we're trying to run this application, we've receiving `ImportError`

    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    ImportError: No module named mime.multipart

#### What's happening
We've mixed Standard Library module called `email` with local module `email.py`. In this case, application sees local module, and imports it, instead of expected one.

#### Solution
In this case, we have to be very careful. Python uses pre-defined order of [importing modules][7]. When we're trying to import `spam` it looks in:

* built-in module (string, re, datetime, etc.)
* searches for a file named `spam.py` in directories given by the variable `sys.path` in
 - the directory containing the input script (or the current directory).
 - PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).
 - the installation-dependent default.

### Bonus Mistake: Differences between Python 2 and Python 3:
Simple thing can make a big difference. Python 3 handles exception in [local scope][8].

    import sys

    def bar(i):
        if i == 1:
            raise KeyError(1)
        if i == 2:
            raise ValueError(2)

    def bad():
        e = None
        try:
            bar(int(sys.argv[1]))
        except KeyError as e:
            print('key error')
        except ValueError as e:
            print('value error')
        print(e)

    bad()

#### Current behaviour
`Python 2`

    $ python foo.py 1
    key error
    1
    $ python foo.py 2
    value error
    2

`Python 3`

    $ python3 foo.py 1
    key error
    Traceback (most recent call last):
      File "foo.py", line 19, in <module>
	bad()
      File "foo.py", line 17, in bad
	print(e)
    UnboundLocalError: local variable 'e' referenced before assignment

#### What's happening
When an exception has been assigned to a variable name using `as target`, it is cleared at the end of the except clause:

    except E as N:
        try:
            foo
        finally:
            del N

This means the exception must be assigned to a different name to be able to refer to it after the except clause. Exceptions are cleared because with the traceback attached to them, they form a reference cycle with the stack frame, keeping all locals in that frame alive until the next garbage collection occurs.

[1]: http://www.toptal.com/python/top-10-mistakes-that-python-programmers-make
[2]: http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments
[3]: http://docs.python-guide.org/en/latest/writing/gotchas/#late-binding-closures
[10]: http://www.onlamp.com/pub/a/python/2004/02/05/learn_python.html?page=2
[4]: http://legacy.python.org/dev/peps/pep-0253/
[5]: https://docs.python.org/2/tutorial/errors.html#handling-exceptions
[6]: https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
[7]: https://docs.python.org/2/tutorial/modules.html#the-module-search-path
[8]: https://docs.python.org/3/reference/compound_stmts.html#except
