# How to test it?
## Szymon Pyżalski

Everyone knows that it is good to write unit tests. But how to write good ones?
The key is first to understand what the unit tests are for. Then to write them
keeping this in mind. Let's look at the main purposes that unit tests serve and
think about the way to fulfill them as much as possible.

### Testing *user stories*

Let's look at some *user stories* of different people profiting from the
existence of unit tests.

#### 1. As a current developer I want the test to guide my coding.

This is *your* story the moment you write the test. You want the test to be the
first check if your design makes sense. You want it then to answer if you
implemented this design correctly. At last you want to make sure if you really
covered all the edge cases your code can encounter.

#### 2. As a future developer I want to see if I don't break existing features.

This is the story of your *future self*. Or a story of your colleague or
or a contributor. This is also the reason the product owner sleeps well under
the green light of Jenkins monitor.

#### 3. As a library/framework user I want to use the tests as documentation.

The story of a user that wants to see an example usage of your code. And your
*future self* as well.

### How would good tests look like?

#. Cover as much cases as possible.
#. Be as real-life as possible.
#. Check *all* the important effects of the code.
#. Check *only* what is important.
#. Be as stable as possible.
#. Be comprehensible to human.

### Some techniques...

#### Aim for 100% coverage, but don't think it is enough.

You should reach 100% coverage of your tests. However this isn't a proof for
handling all the cases. The coverage tool won't replace your brain.

#### Write regression tests for bugs spotted by humans.

If you get a bug spotted by a human tester or user, write a test for his case.
Avoid the shame of a bug coming back in future releases.

#### Write fixtures that resemple real-life examples.

Make sure that your fixtures resemble what your application will really see
in production. Use proper scale, character sets etc. Passing a test for 'foo'
and 'bar' might be not sufficient.

#### Use mocks for side-effects.

If your code has side effects, you should check it with mocks. You should in
no way allow for one test case to affect the other. Mock the db state, APIs and
streams in ``setUp``. Clean up after yourself in ``tearDown``.

#### Write cases that check only the feature you want to test.

You shouldn't write tests that are *too* precise. If you e.g. want to check if
your code adds a class to HTML element, get this element from the tree and
check it's ``class`` attribute. Don't use ``assertHTMLEqual`` and similar. This
way you lose stability and your tests won't be able to serve the second user
story.


#### Make the tests clear, what they do.

Write your tests similarly to the production usage of your code. Use
comprehensive docstrings. Make sure that you can look at the test and say "Oh,
I know how to use it".

#### Create yourself reusable utilities for what you do.

If you can, write ``TestCase`` subclasses to inherit from, your own ``assertX``
functions and decorators for your tests. This will help you achieve clarity and
stability of your test cases.

#### Write tests in your documentation.

Make sure your documentation is right and up-to-date by using doctests and
sphinx testing. An example is more comprehensive than literary explanation. And
you don't want to mislead the user.

### Tools


* [http://nose.readthedocs.org/en/latest/](http://nose.readthedocs.org/en/latest/) - nose. One of the most popular test runner for python. It will perform test
discovery, write reports for results and coverage (via plugin).
* [https://pypi.python.org/pypi/mock](https://pypi.python.org/pypi/mock) - mock. A powerful framework that allows you to create mock objects and patch
existing libraries safely.
* [http://sphinx-doc.org/ext/doctest.html](http://sphinx-doc.org/ext/doctest.html) sphinx. Allows you to put the tests in a natural flow of your documentation. These tests will serve both as examples for human and as automated test suite.
* [http://pytest.org/latest/](http://pytest.org/latest/) - py.test. Alternative python test runner. Not recommended by the author, but worth knowing.
