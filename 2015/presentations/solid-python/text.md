# SOLID Python - Ignacy Sokołowski

SOLID is an acronym for five basic principles of Object Oriented Programming.
The principles intend to make software entities easy to understand, maintain,
extend, unit-test and reuse in different contexts.

They are mostly used in strongly typed languages such as Java or C++. Probably
that's why Python developers don't follow them too often or they do but didn't
ever realize it.

In this article, I will briefly explain three of the SOLID principles and show
you how to follow them in Python code.

**SOLID** is actually an acronym of acronyms:

* **SRP** - Single Responsibility Principle
* **OCP** - Open/Closed Principle
* **LSP** - Liskov Substitution Principle
* **ISP** - Interface Segregation Principle
* **DIP** - Dependency Inversion Principle

The principles were collected by Robert C. Martin, also known as "Uncle Bob",
in early 2000s.


## Single Responsibility Principle

The Single Responsibility Principle states that every class should be
responsible for only one thing. We could also extend it to methods and in
languages like Python, to functions.

What does it mean to be responsible for only one thing?

### Not just to "do only one thing"

Say you have a function for sending e-mail reports. It gets data for the
report, then formats it and finally sends it via e-mail.

So, it does three different things.

But if each of these three things is implemented in a separate function and
the main function just calls them, then it will not be responsible for how
they are implemented.

```python
def send_email_report(email, time_period):
    report = prepare_report(time_period)
    report_body = format_report(report)
    send_email(email, report_body)
```

The function above does not have to know how to get the data nor how to format
the report. It just tells these functions to do their job. It is also easier
to see the flow of this function, when you are not distracted by details. If
you want to see how exactly the report is formatted, you can look at the
``format_report()`` function.

### One level of abstraction

The function for sending e-mail reports is responsible for only one level of
abstraction.

In order to send a report, we need to perform three tasks.

* Get the data
* Format the report
* Send it via e-mail

So, here just *sending report* is the highest level of abstraction and it
performs three tasks on a lower level of abstraction. Each of these three
tasks need to perform several different tasks on an even lower level.

To get the report data, we need to:

* Build an SQL query
* Send the query to a database
* Parse the results on data objects

Each of these tasks will be implemented in a separate function and they all
will be invoked by ``prepare_report()``, the same way as
``send_email_report()`` does.

### One reason to change

Uncle Bob defines responsibility as a reason to change. So, a class or
function should have no more than one reason to change.

If you'd like to change the way reports are formatted, you should not need to
change the class responsible for preparing report data. If you'd like to
change the database for articles, you should not need to change controller
for displaying them.

In our example, if we'd like to change the way reports are formatted, we
change only the ``format_report()`` function. ``send_email_report()``,
``prepare_report()`` and ``send_email()`` stay untouched.


## Open/Closed Principle

As I mentioned at the beginning of the article, one of the goals of SOLID is
extensibility. If we'd like to introduce a new class which differs from an
existing one by only a small detail, we should not have to copy all the code
from one class to another.

The Open/Closed Principle states that "software entities (classes, modules,
functions, etc.) should be open for extension, but closed for modification".

In our example, we have a function for formatting reports.

The ``send_email_report()`` function explicitly calls ``format_report()``. If we
wanted to change the way reports are formatted, we would change the
``format_report()`` function. That's OK if it's in our own codebase and if
we always want to format reports in the same way.

But what if all these functions are in a third party library and we can only
import and call them? Then, the only way to change the way of formatting
reports would be to implement our own version of ``format_report()`` and then,
to rewrite ``send_email_report()`` to invoke it.

If the code is in our own codebase, there could be another problem with
extending it. What if we had two different report formats? Sometimes we want
to use the existing ``format_report()`` function, so we don't want to change
it. But sometimes we'd like to use another one. There's no way to tell
``send_email_report()`` to format reports differently.

It means that our function is closed for extension. It is also automatically
open for modification because the only way to use a different report formatter
is to modify our function.

One of the advantages of classes over functions is that they can be easily
extended by inheritance. We could move our functions into methods of a class:

```python
class EmailReporter:

    def report(self, email, time_period):
        report = self._prepare_report(time_period)
        report_body = self._format_report(report)
        self._send_email(email, report_body)

    def _prepare_report(self, time_period):
        # ...

    def _format_report(self, report):
        # ...

    def _send_email(self, email, body):
        # ...
```

Now, if we'd like to modify the way of formatting reports, we can create a
subclass and override or extend only one method:

```python
class EmailReporter2(EmailFormatter):

    def _format_report(self, report):
        # The new implementation.
```

But that's not the best way to go. We're back to the problem of a class with
more than one responsibility. There could be more than one place where we
send messages to our users. We wouldn't like to use ``EmailReporter`` to send
newsletter or registration e-mails.


## Dependency Inversion Principle

Our functions are dependent on each other. The problem is the way the
dependencies are defined. In fact, they are now hard-coded into the
``send_email_report()`` function.

The Dependency Inversion Principle proposes to invert the way we define
dependencies. Instead of defining them inside function or method definitions,
we should be able to set them from outside. How can we do that?

One way would be to use dependency injection. We could add new arguments
to ``send_email_report()`` which would specify which functions to use:

```python
def send_email_report(
        email, time_period,
        prepare_report, format_report, send_email):
    report = prepare_report(time_period)
    report_body = format_report(report)
    send_email(email, report_body)
```

I personally don't like injecting dependencies into functions or methods as it
pollutes function's interface and requires me to pass all the dependencies
every time I want to use the function.

A better way would be to use a class instead of a function:

```python
class EmailReporter:

    def __init__(self, report_preparator, report_formatter, email_sender):
        self._report_preparator = report_preparator
        self._report_formatter = report_formatter
        self._email_sender = email_sender

    def report(self, email, time_period):
        report = self._report_preparator.prepare(time_period)
        report_body = self._report_formatter.format(report)
        self._email_sender.send(email, report_body)
```

Now, the public interface for ``EmailReporter.report()`` does not include
dependencies. No matter what report formatter we want to use, we invoke it the
same way. We don't have to pass the dependencies in every call.

As long as our class is stateless, we can create one instance of it for each
variation of dependencies:

```python
# Common dependencies
report_preparator = ReportPreparator()
email_sender = EmailSender()

# Two kinds of reporters
email_reporter_html = EmailReporter(
    report_preparator=report_preparator,
    report_formatter=HTMLReportFormatter(),
    email_sender=email_sender,
)
email_reporter_pdf = EmailReporter(
    report_preparator=report_preparator,
    report_formatter=PDFReportFormatter(),
    email_sender=email_sender,
)
```

And we can call ``email_reporter_html.report(email, time_period)``
for any e-mail address or time period.


### Stateless classes

For many Python developers, this kind of class can look a bit weird. We
usually use classes only when we need to manage the state of an object.
Otherwise, we just use pure functions.

It is important to understand the difference between two types of objects:
those that store and represent data, and those that perform some actions.

The former ones store data in their attributes. They don't even have to expose
any public methods, the most important job they do is to aggregate data into
one object.

```python
class Person:

    def __init__(self, first_name, last_name, email, gender, spouse=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.spouse = spouse
```

If they have any public methods, they should not interact with the outside
world. They should either change the object's state or return some data
computed from the object's attribute values:

```python
class Person:

    def __init__(self, first_name, last_name, email, gender, spouse=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.spouse = spouse

    @property
    def is_male(self):
        return self.gender == 'male'

    @property
    def is_female(self):
        return self.gender == 'female'

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def marry(self, fiancee):
        self.spouse = fiancee
        if fiancee.is_male:
            self.last_name = fiancee.last_name
```

If we needed to be able to send e-mails to a ``Person``, we should not
implement ``send_email()`` method in the ``Person`` class but rather create a
new ``EmailSender`` class with ``send()`` method, to which we would pass a
``person`` instance or just its e-mail address.

Why not to pass the person's e-mail to ``EmailSender.__init__``? Because then
we would need a separate sender for every e-mail recipient. Otherwise, we can
have only one instance to send e-mails to any person. We don't ever have to
instantiate ``EmailSender`` in a method where we want to send an e-mail.

``EmailSender`` is the second type of class: the one that can perform an
action. Such classes act like functions. Since we want to follow the SRP, they
will usually have only one public method. The only thing that varies them from
functions is the possibility to configure them during instantiation.

Note that in Python, if a class implements ``__call__()`` method, its instance
does not differ at all from a regular function. We could do that with our
``EmailReporter`` class by renaming its ``report()`` method to ``__call__()``.
You could treat such classes as factories of functions:

```python
send_email_report = EmailReporter(...)
send_email_report(email, time_period)
```

### Interfaces

When one class needs to use another class to perform a task, it accepts it as
an argument to the ``__init__`` method. It does not know of what type the
dependency will be. The only thing it has to know about the dependency is the
interface of its public methods.

Many times I have seen injecting dependencies as classes rather than as
instances, for example:

```python
class EmailReporter:

    def __init__(self, report_formatter_class, ...):
        self._report_formatter = report_formatter_class()
```

Here we depend on signature of the class's ``__init__``. It is important to
know that the initializer is not a part of the public interface. We could
have many different formatters which will require different arguments to be
constructed but as long as they share the same signature for public methods,
they implement the same interface.

The ``EmailReporter`` requires a report formatter. It does not care what type
of reporter will be provided so it does not know its concrete type nor the
arguments to its ``__init__`` method.

```python
class EmailReporter:

    def __init__(self, report_formatter, ...):
        self._report_formatter = report_formatter
        # [...]

    def report(self, email, time_period):
        # [...]
        self._report_formatter.format(data)
        # [...]
```

It only knows that it will have a ``format()`` method which accepts one
argument. Thanks to this, it is easy to implement any kind of formatter that
will satisfy the reporter.

```python
class MarkdownReportFormatter:

    def format(self, report):
        offers = '\n\n'.join([
            '## {offer.title}\n\n{offer.text}'.format(offer=offer) for
            offer in report.offers
        ])
        return '# {title}\n\n{offers}'.format(
            title=report.title,
            offers=offers,
        )
```

```python
class JinjaTemplateReportFormatter:

    def __init__(self, environment, template_name):
        self._environment = environment
        self._template_name = template_name

    def format(self, report):
        template = self._environment.get_template(self._template_name)
        return template.render(report=report)
```

We have two different formatters with two different initializers.
As they share the same signature for the ``format()`` method, we can use both
of them as a dependency for the ``EmailReporter``:

```python
EmailReporter(
    report_preparator=ReportPreparator(),
    report_formatter=MarkdownReportFormatter(),
    email_sender=EmailSender(),
)
EmailReporter(
    report_preparator=ReportPreparator(),
    report_formatter=JinjaTemplateReportFormatter(
        environment=jinja2.Environment(
            loader=jinja2.FileSystemLoader('path/to/templates'),
        ),
        template_name='report.html',
    ),
    email_sender=EmailSender(),
)
```

### Loose coupling

The main goal of the Dependency Inversion Principle, is to help writing loosely
coupled software. If our modules and classes are less coupled, it is easier to
change a part of code without a need to touch the other parts. Modules also
become portable and easier to test.

You have already noticed that our classes for sending e-mail reports do not
depend on each other. The ``EmailReporter`` does not know about the existence
of the ``HTMLReportFormatter`` nor about the ``EmailSender``. If we implemented
each of these classes in a separate module, the modules would not import from
each other.

Our classes automatically become more reusable. As the ``EmailSender`` does
not know that it will send reports, it can be used to send any kinds of
e-mail messages. Thanks to low coupling of modules, classes can be easily
ported between different projects. If we have multiple applications where we
send e-mails, we can release our ``EmailSender`` in an external library.

### Testing

When we want to unit-test classes in isolation, we often use mocking.
We use ``mock.patch()`` to patch the behavior of a method which should not be
executed in a particular test. When our classes have many dependencies which
are tightly-coupled, we need to patch a lot.

If we wanted to test our ``send_email_report()`` function, we would need to
patch ``prepare_report()``, ``format_report()`` and ``send_email()`` in every
test. We need patching because the code is closed for extension.

On the other hand, if we wanted to unit-test the ``EmailReporter``, instead
of mocking, we could simply pass different instances of our dependencies than
those used in production code.

```python
reporter = EmailReporter(
    report_preparator=FakeReportPreparator(),
    report_formatter=FakeReportFormatter(),
    email_sender=FakeEmailSender(),
)
```

If we don't want to create fake classes just for the sake of testing, we can
still use mocks but we don't have to patch.

```python
report_preparator_mock = mock.create_autospec(ReportPreparator)
report_preparator_mock.prepare.return_value = Report(...)
report_formatter_mock = mock.create_autospec(ReportFormatter)
report_formatter_mock.format.return_value = '<formatted report>'
reporter = EmailReporter(
    report_preparator=report_preparator_mock,
    report_formatter=report_formatter_mock,
    email_sender=mock.create_autospec(EmailSender),
)
```

Our unit-tests can now focus on behavior of the class under test and are
independent of the other classes. But are such tests enough to be sure that
our software works as expected? Of course not. We also need to test if the
classes which we tie together for production code, integrate with each other
as expected. That's what we do in integration tests.

Loose coupling helps us to separate unit-tests from integration tests.
Unit-tests assert that a single class's logic is correct. Such tests can be
ported to any other project along with the class under test as they are
independent of the whole application and the context in which it is used.

Integration tests are written against production-ready instances, with all the
dependencies set. In our case, we would write integration tests for
the ``email_reporter_html`` instance, where we would patch only the e-mail
server. Such tests also make sure that the functionality of e-mail reporting
works even if we change the report formatter or the data preparator.

### Dependency Injection Container

OK, now when we have our loosely coupled classes, we have to somehow wire them
together. Where should we do that?

Dependency gluing should be done at the highest level, nearest the main entry
point of your application. If it's a simple application, you can do that
manually, for example in your ``main()`` function:

```python
def main(args=sys.argv):
    config_path, email, time_period = args[1:]

    config = parse_config_file(config_path)
    db = Database(url=config['db_url'])
    offers = OfferRepository(db)
    email_reporter = EmailReporter(
        report_preparator=ReportPreparator(offers=offers),
        report_formatter=JinjaTemplateReportFormatter(
            environment=jinja2.Environment(
                loader=jinja2.FileSystemLoader(config['templates_dir']),
            ),
            template_name='report.html',
        ),
        email_sender=EmailSender(
            smtp_uri=config['smtp_uri'],
            from_address=config['from_email'],
        ),
    )

    email_reporter.report(email, time_period)

if __name__ == '__main__':
    main()
```

But as the number of your dependencies and connections between them grow, it
will no longer be so easy to maintain them in this form. That's the moment
when you need a Dependency Injection Container.

DI Container is an object which stores all the dependencies of your application
in one place. There are multiple implementations of containers in several
programming languages like Java, .NET, PHP, and even in Python.

Here's an example of a Knot container:

```python
def make_container(config):
    c = knot.Container(config)

    @knot.service(c)
    def db(c):
        return Database(url=c['db_url'])

    @knot.service(c)
    def offers(c):
        return OfferRepository(db=c('db'))

    @knot.service(c)
    def report_preparator(c):
        return ReportPreparator(offers=c('offers'))

    @knot.service(c)
    def jinja_env(c):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(c['templates_dir']),
        )

    @knot.service(c)
    def report_formatter(c):
        return JinjaTemplateReportFormatter(
            environment=c('jinja_env'),
            template_name='report.html',
        )

    @knot.service(c)
    def email_sender(c):
        return EmailSender(
            smtp_uri=c['smtp_uri'],
            from_address=c['from_email'],
        )

    @knot.service(c)
    def email_reporter(c):
        return EmailReporter(
            report_preparator=c('report_preparator'),
            report_formatter=c('report_formatter'),
            email_sender=c('email_sender'),
        )

    return c
```

And here's how to use it:

```python
def main(args=sys.argv):
    config_path, email, time_period = args[1:]

    config = parse_config_file(config_path)
    dependencies = make_container(config)

    dependencies('email_reporter').report(email, time_period)

if __name__ == '__main__':
    main()
```

One of the advantages of such container is that you can give it different
configuration for tests and write integration tests against particular
dependencies.

```python
def test_email_reporter():
    container = make_container({'db_url': 'sqlite:///'})
    email_reporter = container('email_reporter')
    email_reporter.report(...)
```


# Summary

For some of you, this way of thinking about object-oriented design may be
completely new and quite shocking. You may find it "not pythonic" or think
that it's over engineering.

I was shocked too, when I first saw it. It was not easy to get rid of my old
habits. But I decided to try it out and now I see how much easier programming
and testing can be when applying these principles, especially when I'm working
on a rapidly growing project for which requirements and business decisions
change quite often.

What I showed you in this article, is just the tip of the iceberg. I encourage
you to read more about SOLID principles and design patterns. I promise it will
pay off!


# Further reading

* Robert C. Martin - "Design Principles and Design Patterns"  
 http://www.objectmentor.com/resources/articles/Principles_and_Patterns.pdf
* Robert C. Martin - "Agile Software Development: Principles, Patterns, and
  Practices"
* Robert C. Martin - "Clean Code. A Handbook of Agile Software Craftsmanship"
