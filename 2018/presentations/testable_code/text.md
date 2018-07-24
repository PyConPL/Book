# Testable code. A story about making the (testing) world better

## Abstract
What does it mean to have a testable code? 
In general, it means, that the code is easy to test and it is easy to set up a testing environment. 
Sometimes it is tough to make the code testable, especially in a large, legacy codebase, 
but I'd like to tell you some approaches and tips, that could help you to make your code more maintainable, 
understandable and reliable. 

Currently, I'm working on splitting a big legacy monolith into a small and handy microservices. 
This kind of activity often goes together with refactoring and fixing old problems. 
If we are starting with a fresh new project, then why not to do things right (again?!) at the beginning?

<img src="do-things-right.jpg">

My story is about some notorious programming problems I was facing and how these problems were fixed.

## Global variables

Global variables are variables with global scope, which means, that they are accessible from any place of the program in general. I’ll be sloppy and will not talk about some exceptions, because they are not changing the overall picture.

```python
var = 0

def increment():
    global var
    var += 1
```

or:

```python
class Holder:

    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1


shared_holder = Holder()


def increment():
    shared_holder.increment()
```

or even:

```python
# database.py
engine, db = create_db('<URI>')

# another.py
from .database import db  # `create_db` is called during the import 
```

Does it seem familiar to you?
Global variables are not bad but often used in a wrong context. Context is the thing that matters. 
We got to use proper tools in proper places. Let's look at what happens when global variables are misused.

### It is hard to test

Having global variables is making harder to set up a clean environment for a test. 
It means that global state is shared across test runs.
If you change a global state, then you'll have to reset it for the next test, and so on.

```python
def test_increment():
    shared_holder.increment()
    assert shared_holder.value == 1


def test_decrement():
    shared_holder.decrement()
    assert shared_holder.value == -1
```

The fact causes the failure that shared_holder object is the same in both tests. 
Which test will fail in this suite depends on the execution order, and it is also wrong.

### Makes thread-safety implementation more complicated
Having global variable accessible by multiple threads often imply usage of synchronization mechanisms, that 
makes the code more complicated and also affects performance.

Naive and not thread-safe version:

```python
import threading
import time


def increment():
    for i in range(500000):
        shared_holder.increment()


if __name__ == '__main__':
    start = time.time()
    threads = [threading.Thread(target=increment) for i in range(2)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(shared_holder.value)
    print(time.time() - start)
```

```bash
$ python not_thread_safe.py
889706
0.2428889274597168
```

Thread-safe version:

```python
class Holder:

    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1
```

```bash
$ python thread_safe.py
1000000
0.49862122535705566
```

->If anybody can change it - you can't rely on it.<-

Thus being said using a global state usually makes the program less predictable and more complicated. 
Also, it makes debugging harder since it will be harder to detect who changed a global variable.
And consecutively it makes people less interested in writing tests or refactoring.

But, you can’t entirely avoid a global state, because something always is global.
For example, the runtime environment is global. Your `os`, `sys` are all in this category
It is handy to use global variables in small and simple programs with a few modules if it doesn't introduce complexity 
mentioned above, or at least this behavior is isolated and manageable.

## How to (not) fix it
In some cases, to make things work, you could monkey patch the module where the global object is with a newly created object.
In large projects, it could lead you to a significant amount of monkey patching different modules.

```python
# holder.py
# Holder class & global variable from above

# decrementer.py
from .holder import shared_holder


def decrement():
    shared_holder.decrement()

# test_holder.py
import pytest

from . import decrementer
from . import holder


@pytest.fixture
def new_holder():
    return holder.Holder()


@pytest.fixture(autouse=True)
def patched(monkeypatch, new_holder):
    monkeypatch.setattr(decrementer, 'shared_holder', new_holder)


def test_holder():
    holder.shared_holder.increment()
    assert holder.shared_holder.value == 1


def test_decrementer():
    decrementer.decrement()
    assert decrementer.shared_holder.value == -1
```

In the example above the `monkeypatch` fixture from `py.test` is used. 
It allows you to modify objects and rollback these changes automatically.

The `patched` fixture monkey patches the loaded module with freshly created `Holder` instance. 
If you remove this fixture, then `test_decrementer` will fail, because it will use a global variable, 
that changed in `test_holder`.

In this situation, we have only two tests, and we need to add special machinery to make things work. 
If there will be more modules where the global state could change, the complexity will increase dramatically. 
As a project grows very soon, it will be almost impossible to know where and the global state was changed. 
Fixing these things will be even harder, especially if you have dynamic imports and global things are 
initialized on import.

Besides of enormous amount of patching it makes your tests weaker, because they cover the situation, that is farther
away from the real setup. And it will decrease an actual code coverage. Also, the test suite becomes more fragile, since some tests could depend on the execution order.

->It could fix some symptoms, but it doesn't fix the problem.<-

The global state in the previous examples is hardly predictable. Let's change it and make it manageable. 
The first step is to take control when the object is initialized. We want to initialize it only when we need it, just in the desired context. This type of refactoring is known as «Extract Method»

## Deferred initialization. Flask example
Flask has a beautiful example of solving this problem - `init_app` pattern. 
It allows you to isolate some global state in an object and control when to initialize it. 
Also, it usually used to register some teardown logic for this global object.

```python
# extension.py
class Extension:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('CONFIG', 'value')
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ...

ext = Extension()

# app.py
...
ext.init_app(app)
```

In our project, the most problematic global state was the DB. We're using `pytest` and the database initializes during importing things in top-level `conftest.py`. Then testing database was initialized as a fixture, and all modules used in the project were monkey patched with this new object. Let's see how our code could be 
changed with `Flask-SQLAlchemy` extension, that provides `init_app` pattern:

Before:

```python
# database.py

engine, db = create_db(settings.db_url)

# app.py

application = App(__name__)

# conftest.py
import database


@pytest.fixture(scope='session', autouse=True)
def db_schema(db_url):
    engine = create_engine(db_url)

    # Create extensions, tables, etc

    Session = orm.scoped_session(orm.sessionmaker())
    Session.configure(bind=engine)
    session = Session()

    yield session

    Session.remove()
    # Drop tables, extensions, etc


@pytest.fixture
def db(db_schema, monkeypatch):
    db_schema.begin_nested()
    monkeypatch.setattr(database, 'db', db_schema)

    yield db_schema

    db_schema.rollback()
    db_schema.close()
```

After:

```python
# database.py
db = SQLAlchemy()

# app.py

application = App(__name__)

from .database import db

db.init_app(application)

# conftest.py
from .app import application
import database


@pytest.fixture(scope="session")
def db():
    # Create extensions, tables, etc
    yield database.db
    # Drop tables, extensions, etc


@pytest.fixture(autouse=True)
def session(db):
    db.session.begin_nested()
    yield db.session
    db.session.rollback()
```

Now the database is initialized only when the application initializes - we put the DB into application context. 
As a consequence, we don't have to initialize another database connection in tests and make monkey patching. 
We're managing this global state - we create a session on demand, only when it is needed.

## Factories
But `application` is still global, and it initializes on import. If we did not initialize the DB before running the tests, it wouldn’t work. To address this problem the application factory pattern exists. The basic idea is to isolate `application` instance creation in a separate function. There are a few benefits of doing that:

- Isolate side-effects of creating an application on module-level
- Flexibility - multiple apps or/and different settings

```python
# app.py
def create_app(settings_object, **kwargs):
    flask_app = Flask(__name__)
    flask_app.config.from_object(settings_object)
    flask_app.config.update(**kwargs)

    from .database import db

    db.init_app(flask_app)
    db.app = flask_app

    return flask_app

# conftest.py
from app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app("app.settings.TestSettings")


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def db(app):
    # Create extensions, tables, etc
    yield database.db
    # Drop tables, extensions, etc
```

Benefits:
- An application instance is created after the test session start
- It is available as a fixture, which gives more flexibility (e.g., parametrization)

## Running speed vs. test isolation
We fixed the global state on the Python level, but the database itself is a shared resource. 
It should be in the same state before each test run.

There are a couple of ways of doing this:
- Creating DB for each test case (slow/isolated)
- Recreate all tables & stuff for each test case (faster / less isolated)
- Wrap each test case in a transaction and rollback it at the end of a test case (fastest, even less isolated)

Each approach has its pros and cons, but the main trade-off is speed vs. test isolation. To be entirely sure, that
each test case is isolated you can create a new database for each test case, but it will be very slow.
You can recreate all the tables for each test case, it will be faster, but you'll have to take care about re-creating stuff
you need for the tests - views/triggers / etc.. Usually, it is pretty easy to do with migrations.
Or you could create a transaction for each test case and roll it back in the end - super fast, but what if you need to
test some logic, that involves transaction manipulations? For example, Django has `TransactionTestCase` and `TestCase`
for dealing with different situations. `TransactionTestCase` truncates all tables and `TestCase` rolls back
 a transaction.

## Dependency injection
There is another technique that was used in the previous examples but wasn't mentioned explicitly.
Dependency injection.

It is a software design pattern which allows you to isolate some logic into a separate entity and pass it into another one as a dependency. Example:

```python
class BadAirplane:
    max_speed = 900
    distance = 14800

    def fly(self):
        print('Fly {distance} in {time} hours'.format(distance=self.distance, time=self.distance / self.max_speed))

# vs

class Engine:
    
    def __init__(self, max_speed, distance):
        self.max_speed = max_speed
        self.distance = distance

    @property
    def flying_time(self):
        return self.distance / self.max_speed
    

class GoodAirplane:

    def __init__(self, engine):
        self.engine = engine
        
    def fly(self):
        print('Fly {distance} in {time} hours'.format(distance=self.engine.distance, time=self.engine.flying_time))
        

if __name__ == '__main__':
    engine = Engine(900, 14800)
    plane = GoodAirplane(engine)
```

Now you can pass any engine you want to the airplane and test its logic with different engines, or mock your engine if it is too heavy for an ordinary test. Applying this approach allows you to decouple execution of a task from implementation.

For example, you could isolate some hard-to-test logic (for example 3rd party service or some heavy computations)
in this "dependency" and pass a mock object in tests instead of the real one.

In Flask it allows you to write isolated extensions with ease, in pytest you can reuse and parametrize fixtures in tests.

## Data & logic separation
When you're writing tests, usually you use some values as input for your testing logic, and you expect 
some other values to be an output of this logic: 

```python
def test_something():
    assert something('a', 'b') == 'c'
```

But when you hardcode them inside the testing code, it makes it less extendable. If you keep test data separate from
the test logic, it will make modifications much more manageable. Dependency injection is in the game again!

```python
@pytest.mark.parametrize(
    'first, second, expected', 
    (
        ('a', 'b', 'c'), 
        ('b', 'a', 'd')
    )
)
def test_something(first, second, expected):
    assert something(first, second) == expected
```

It is especially helpful if you have an extensive test suite - it could help you to see similarities in your tests and 
refactor them or build some reusable tools, that will help you in the future.

## Factories
But what if the object you're testing is more complicated than a string? `SQLAlchemy` model for example.
You could create them manually in a separate fixture, or you could use something like `Factory boy`.

```python
class User(Base):
    id = Column(Integer(), primary_key=True)
    name = Column(Unicode(20))


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    name = 'John Doe'
```

Usage is straightforward:

```python
>>> UserFactory()
<User: User 1>
>>> session.query(User).all()
[<User: User 1>]
```

Factory boy is very well integrated with py.test with absolutely gorgeous `pytest-factoryboy` just register your factories and make sure that they are imported in your test suite (in the root `conftest.py` for example):

```python
from pytest_factoryboy import register


@register
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    ...
```

and now you magically have `user` and `user_factory` fixtures.

```python
def test_model_fixture(user):
    assert user.name == 'John Doe'


def test_factory_fixture(user_factory):
    assert user_factory().name == 'John Doe'
```

The `user` fixture corresponds to a simple factory call without arguments. 
`pytest-factoryboy` provides a lot of different features, that are worth checking out.

## Why you should try TDD
Just a brief recap, what TDD is:

1. Write a failing test
2. Add/modify the code so that the test pass
3. Refactor test & code

Why? It just saves time and consequently money. For example, you're building a new API with Flask, and you want to add
a users listing in the beginning:

```python
def test_users_listing(client):
    response = client.get('/users')
    assert response.status_code == 200
```

This test will fail, but you'll know why - there is no such route in your app. Add it with a minimal stub handler and
your test will pass. Ok, but we actually need users in the response:

```python
def test_users_listing(client, user):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json == [{'id': user.id, 'name': user.name}]
```

Then update your handler with the code, that will query users, and the test will pass. 
After that, you do the next feature in the same way, and then another one and so on. In the end, you'll have each feature tested. 

Then, for example, you'd add a new field to the user - `age`. You'll write a test for it, and it will pass. But if your listing
will not restrict the output fields the listing test will fail after adding `age` field - you broke the interface, but luckily you'll know about as soon as you run your tests. Fix it in the way you want and go to the next feature. 

Rapid and iterative development process - is a beautiful feature of TDD. You'll see problems very fast just by running a test suite. With pytest you don't even have to re-run it - you could use looponfailing mode from `pytest-xdist` plugin:

```bash
pytest -f tests
```

Also, you'll trust your test suite, and in the case, if something will fail on production, you'll add a regression test.
It makes your more confident about your code when you're doing refactoring or adding a new feature. 
You'll know that the new feature will not break other features and it is safe to add.

It could help you with building something big - split this big thing into small functional pieces, write tests and make them pass. 

But it is not a silver bullet. It doesn't mean that you don't have to write other types of tests or don't use different approaches.
Sometimes it is just more straightforward to do something in the way you are comfortable to do. 
But consider adding TDD to your arsenal, it worth trying to improve your developer experience.

References:
- http://wiki.c2.com/?GlobalVariablesAreBad
- https://www.toptal.com/qa/how-to-write-testable-code-and-why-it-matters
- http://flask.pocoo.org/docs/1.0/extensiondev/
- http://flask.pocoo.org/docs/1.0/patterns/appfactories/
- http://python-dependency-injector.ets-labs.org/introduction/di_in_python.html
- https://dmerej.info/blog/post/why-you-should-try-tdd/
- http://blog.cleancoder.com/uncle-bob/2016/03/19/GivingUpOnTDD.html