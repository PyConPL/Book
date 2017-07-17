# Parametrize all the tests! (workshop)

In this workshop you will learn about **pytest** [1] and why it is better than
unittest or nose. You will see and try out examples on easy and later on more
complex scenarios. You will learn how to write parametric tests and you will
paramterize some test for a common problem such as fizzbuzz. Later we'll dive
in into fixtures and how they are different than setup and teardown. Fixtures
can be parametric as well, so we'll code some examples for that as well.
At the end, you'll learn about cross products of parameters and fixtures.

This text can serve as a brief introduction to the topic, but some of the parts
are intentionally missing and will be presented on the workshop.


## What is pytest

Pytest is a framework for writing tests for your Python code. When you look at
testing in Python, you'll probably learn about **unittest** [2], because it is
a part of Python's standard library. However, unittest is not very flexible and
its syntax and usage is very much inspired with JUnit – a Java unit testing
framework. I guess writing code in Python using a Java inspired API is
something no Pythonista would desire. :punch:

The lack of flexibility when running tests written in unittest inspired another
project to be created, a once popular tool called **nose** [3]. While nose can
make running tests easier and more pleasant, the main part – how do we write
our tests – remained the same. Not to mention nose has been in maintenance
mode for the past several years. :vhs:

**Pytest** on the other hand reinvents the way test are being written.
Instead of Java-like nonsense, you write very readable, Pythonic code. :snake:

Compare this:

```python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
```

With this:

```python
def test_upper():
    assert 'foo'.upper() == 'FOO'

def test_isupper():
    assert 'FOO'.isupper()
    assert not 'Foo'.isupper()
```

Pytest is using a simple assert statement to verify _things_ in tests. Unlike
using assert [4] in regular Python code, it is monkeypatched to provide more
information about what happened when the assertion fails:

```python
def test_upper():
    assert 'foo'.upper() == 'FOo'
```

```
================================== FAILURES ===================================
_________________________________ test_upper __________________________________

    def test_upper():
>       assert 'foo'.upper() == 'FOo'
E       AssertionError: assert 'FOO' == 'FOo'
E         - FOO
E         + FOo

test_example.py:2: AssertionError
========================== 1 failed in 0.02 seconds ===========================
```

## Let's write some tests for fizzbuzz

Fizzbuzz [5] is a group word game for children to teach them about division.
Players take turns to count incrementally, replacing any number divisible by
three with the word "fizz", and any number divisible by five with the word
"buzz". If the number is dividable by both, one shall say "fizzbuzz".

Let's first write a function that takes an integer and returns a string with
"fizz", "buzz", "fizzbuzz" or the number depending on the rules of the game.

```python
# fizzbuzz.py
def fizzbuzz(number):
   ...
```

(The body of the above function is intentionally left out as an exercise for
the reader.)

Let's create a `test_fizzbuzz.py` file in the `tests` directory. When running
`python -m pytest`, the tests in this directory will be automatically collected
if the name of the files starts with `test_`.

```python
# tests/test_fizzbuzz.py
from fizzbuzz import fizzbuzz


def test_regular():
    assert fizzbuz(1) == '1'


def test_fizz():
    assert fizzbuz(3) == 'fizz'
```

Now run the tests with `python -m pytest`. (Note that if you have an virtual
environment set up in the very same directory, pytest will likely try to
collect the tests from within that.  You can either use the `--ignore` switch
to ignore your virtual environment directory or specify the path to your tests
directory as a first positional argument.)

```console
$ python -m pytest --ignore=env
$ python -m pytest tests/
```

Writing tests that check that `fizzbuzz(5)` is `'buzz'` and `fizzbuzz(15)` is
`'fizzbuzz'` is left as and exercise for the reader.

At the end of this part, you should have a fizzbuzz implementation and tests
for 1, 3, 5 and 15.


## Parametrize our tests and why is it better

In reality, we would need to test for other numbers as well, such as 2, 6, 333
etc. Without parametric tests, we have two options:

Copy pasting tests around, renaming them and changing the tested value.

```python
def test_fizz3():
    assert fizzbuz(3) == 'fizz'


def test_fizz6():
    assert fizzbuz(6) == 'fizz'


def test_fizz9():
    assert fizzbuz(9) == 'fizz'
```

Uh... copy pasting code around like that is wrong. :thumbsdown: :poop:

------------

Or running one test over a range of numbers:

```python
def test_fizz():
    for number in (3, 6, 9, 333, 3003):
        assert fizzbuz(number) == 'fizz'
```

This does not look so bad on the first glance, but let us intentionally break
the implementation for large numbers and see how the tests result looks like.


```python
def fizzbuzz(number):
    if number > 100:
        return 'Oh no, a bug!'
    ...
```

From the tests results, do you see what's wrong? :confused:

------------

Instead, we'll paramterize the test. That means, we'll have one test written
– as a template – and it will be run for multiple values.

```python
import pytest


@pytest.mark.parametrize('n', (3, 6, 9, 333, 3003))
def test_fizz(n):
    assert fizzbuz(n) == 'fizz'
```

See what happens when you run the tests and try running them with the verbose
(`-v`) switch.

Let's write parametric tests for all our cases. Note that in our example, we've
used a tuple to represent possible values of our parameter. But it can be any
(terminal) iterable, such as list, set, range or a custom generator.
Try to write some parametric test for fizzbuzz using a range or a (list)
comprehension [6].


## Let's do something more complicated

Imagine we'd have a function that accepts boundaries and returns a generator
of fizzbuzz results, something like this:

```python
def fizzbuzz_range(*args, **kwargs):
    for n in range(*args, **kwargs):
        yield fizzbuzz(n)
```

Now let us write a parametric tests that takes 3 parameters: start, stop and
result:

```python
@pytest.mark.parametrize(['start', 'stop', 'result'],
                         [(0, 3, ['0', '1', '2']),
                          (3, 7, ['fizz', '4', 'buzz', '6']),
                          ...])
def test_fizz(start, stop, result):
    assert list(fizzbuz_range(start, stop)) == result
```

Notice how `@pytest.mark.parametrize` can parametrize multiple values.


## Fixtures and how they work

Sometimes, you want to tests several facts about one thing. Especially if that
thing is hard to create, you might want to prepare it beforehand and use it
repetitively in multiple tests. In that case, you might want to create a
_fixture_ – something that's needed for multiple tests to operate.

Fixture can be created a s a simple function with a decorator:

```python
@pytest.fixture
def game():
    '''A fizzbuzz sequence as in the children's game'''
    return list(fizzbuzz_range(1, 101))
```

Using that fixture from tests boils down to a function parameter with the same
name:

```python
def test_game_has_100_items(game):
    assert len(game) == 100


def test_game_startswith_1(game):
    assert game[0] == '1'


def test_game_endswith_buzz(game):
    assert game[-1] == 'buzz'

...

```

But fixtures are far more powerful than that. They allow you to create a
context for your tests using a `yield` statement. Here is a hypothetical
example where each test using this fixture would connect to a database and
close the connection afterwards:

```python
@pytest.fixture
def db():
    database = ExampleDatabase(user='me', password='test')
    connection = database.connect()
    yield connection
    connection.close()
```

Bare in mind that if a test fails, the last line of this fixture would never
get executed. To make sure the connection get's closed even on failed test,
you would use a classic `try-finally` block:

```python
@pytest.fixture
def db():
    database = ExampleDatabase(user='me', password='test')
    connection = database.connect()
    try:
        yield connection
    finally:
        connection.close()
```

Or, if the database API has a context manager, we could use that as well:

```python
@pytest.fixture
def db():
    database = ExampleDatabase(user='me', password='test')
    with database.connect() as connection:
        yield connection
```

Sometimes, you might want to share a database connection across all the tests,
for that, you might explicitly set fixture's scope. Without specifying a scope,
one fixture is recreated every time a test uses it. Instead, we'll set the
_module_ scope and this time one instance of a fixture is used for all the
tests that require it:

```python
@pytest.fixture(scope='module')
...
```

One fixture can use another fixture, so imagine a scenario, where we want to
reuse a connection for all the tests, but we want to set up database content
before every test and clean it afterwards. We will create 2 fixtures – one
scoped for the module, one with the default scope:

```python
@pytest.fixture(scope='module')
def connection():
    database = ExampleDatabase(user='me', password='test')
    with database.connect() as connection:
        yield connection

@pytest.fixture
def db(connection):
    connection.query(...)  # fill in the data
    try:
        yield connection
    finally:
        connection.query(...)  # delete everything
```

Note that using another fixture from a fixture can be done by using it's name
as a name of a parameter. You can use a module scoped fixture from a default
scoped fixture, but not the other way around (for obvious reasons).


## Already available fixtures in pytest

Not only you can create your own fixtures, but you can benefit form some
fixtures available in pytest by default. You can see the list of them with
`python -m pytest -q --fixtures`.

They include stuff like a temporary directory or more magical things like
`capsys` that allows you to introspect what would normally be printed on
standard output and stderr.

Pytest normally hides every output if the test passes and displays it if the
test fails. This is useful for debugging failed tests. You can leave you prints
in and it doesn't harm. But sometimes you actually want to check would would
have been printed. The `capsys` fixture helps here:

```python
def fizzbuzz_game():
    for n in fizzbuzz_range(1, 101):
        print(n)
```

```python
def test_fizzbuzz_game_prints_100_lines(capsys):
    fizzbuzz_game()
    out, _ = capsys.readouterr()
    assert len(out.strip().split('\n')) == 100
```

------------

You can also use the builtin fixtures to create your own. Here we create a
git repository and let the test execute within:

```python
@pytest.fixture
def gitrepo(tmpdir):
    with tmpdir.as_cwd():
        subprocess.run(['git', 'init'])
        yield tmpdir
```

## Parametrizing fixtures

As well as tests, fixtures can also be parametric [7]. This is very helpful
if you need to run your tests with multiple backends or if you use one
parameter repetitively across multiple tests. Let's get back to our
hypothetical database example and make it parametric:

```python
@pytest.fixture(scope='module', params=['postgres', 'sqlite'])
def connection(request):
    if request.param == 'postgres':
        database = PostgresDB(...)
    else:
        database = SQLiteDB(...)
    with database.connect() as connection:
        yield connection
```

Now every test that uses the _connection_ fixture (even transitively) will run
twice, once with `PostgresDB()` and once with `SQLiteDB()`.

Note that parametric fixtures have a little different syntax and need to accept
the special `request` function parameter that holds the entire context about
the test being run.

------------

In our fizzbuzz example, we might want to test multiple facts about fizzbuzz
calls for 3, 6, 9, 333 etc. Instead of repeating the parameters every time
or creating a global variable with list of numbers, we can crate a parametric
fixture:

```python
@pytest.fixture(scope='module', params=[3, 6, 9, 333])
def fizznum(request):
    return request.param


def test_fizznum_is_not_devidable_by_5(fizznum):
    '''A "metatest" that tests the fizznum fixture itself''''
    assert fizznum % 5 != 0


def test_fizz(fizznum):
    assert fizzbuzz(fizznum) == 'fizz'
```

Notice how we created the fixture module scoped? That's because reusing an
integer cannot harm (it's immutable anyway).


## Cross products of parameters and/or parametric fixtures

All the parameters can be combined together to create a cross product of test
templates. Either you can combine two or more `@pytest.mark.parametrize`
decorators, more fixtures, or both together.

Note that the bellow example is not very well written and I don't encourage to
write code like that, but it serves a purpose. :trollface:

```python
@pytest.fixture(scope='module', params=[3, 6, 9, 333])
def fizznum(request):
    return request.param


@pytest.fixture(scope='module', params=[5, 10, 500])
def buzznum(request):
    return request.param


def test_fizzbuzz(fizznum, buzznum):
    assert fizzbuzz(fizznum * buzznum) == 'fizzbuzz'
```

You can even create a fixture that creates a cross product of fixtures:

```python
@pytest.fixture(scope='module')
def fizzbuzznum(fizznum, buzznum):
    return fizznum * buzznum


def test_fizzbuzz(fizzbuzznum):
    assert fizzbuzz(fizzbuzznum) == 'fizzbuzz'
```

Don't overdo that. If you want to test for all possible values without
_actually testing all possible values_, you might want to look at
**hypothesis** [8].

## Where to go next

I highly recommend reading trough the pytest documentation [1] as it is very
understandable and has plenty of examples. It has multiple sections covering
parametric tests and fixtures. Dive in!

## References

1. pytest documentation. https://docs.pytest.org/
2. unittest in Python documentation. https://docs.python.org/3/library/unittest.html
3. nose documentation. http://nose.readthedocs.io/
4. assert on Python Wiki. https://wiki.python.org/moin/UsingAssertionsEffectively
5. Fizz buzz on Wikipedia. https://en.wikipedia.org/wiki/Fizz_buzz
6. List comprehensions. https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
7. Parametrizing fixtures. https://docs.pytest.org/en/latest/fixture.html#parametrizing-fixtures
8. Hypothesis documentation. https://hypothesis.readthedocs.io/
