# Testable code. A story about making the (testing) world better

## Abstract
What does it mean to have a testable code? 
In general, it means, that the code is easy to test and it is easy to set up a testing environment. 
Sometimes it is really hard to make the code testable, especially in a large, legacy codebase, 
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
Actually, global variables are not bad but often used in a wrong context. Context is the thing that really matters. 
We got to use proper tools in proper places. Let's look at what happens when global variables are misused.

### It is hard to test

Having global variables is making harder to set up a clean environment for a test. 
Basically, it means, that global state will be shared across test runs.
If you change a global state, then you'll have to reset it for the next test, and so on.

```python
def test_increment():
    shared_holder.increment()
    assert shared_holder.value == 1


def test_decrement():
    shared_holder.decrement()
    assert shared_holder.value == -1
```

The failure is caused by the fact, that shared_holder object is the same in both tests. 
Actually, which test will fail in this suite depends on the execution order and it is also bad.

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

But, you can’t completely avoid a global state, because something always is global.
For example, the runtime environment is global. Your `os`, `sys` are all in this category
It is handy to use global variables in small and simple programs with a few modules if it doesn't introduce complexity 
mentioned above, or at least this behavior is isolated and manageable.

## How to (not) fix it
To make things work in some cases you could monkey patch the module where the global object is with a newly created object.
In large projects, it could lead you to a big amount of monkey patching different modules.

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

The `patched` fixture monkey patches the loaded module with freshly created `Holder` instance. 
If you remove this fixture, then `test_decrementer` will fail, because it will use a global variable, 
that was changed in `test_holder`.

In this situation, we have only two tests and we need to add special machinery to make things work. 
If there will be more modules where the global state could be changed, the complexity will increase dramatically. 
As a project grows very soon it will be almost impossible to know where and the global state was changed. 
Fixing these things will be even harder, especially if you have dynamic imports and global things are 
initialized on import.

Besides of huge amount of patching it makes your tests weaker, because they cover the situation, that is farther
away from the real setup. And it will decrease a real code coverage. Also, the test suite becomes more fragile, since some tests could depend on the execution order.

->It could fix some symptoms, but it doesn't fix the problem.<-

The global state in the previous examples is hardly predictable. Let's change it and make it manageable. 
The first step is to take a control when the object is initialized. We want to initialize it only when we need it, 
only in the desired context. This type of refactoring is known as «Extract Method»

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

In our project, the most problematic global state was the DB. We're using `pytest` and the database was 
initialized during importing things in top-level `conftest.py`. Then testing database was initialized as a fixture 
and all modules used in the project were monkey patched with this new object. Let's see how our code could be 
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

Now the database is initialized only when the application is initialized - we put the DB into application context. 
As a consequence, we don't have to initialize another database connection in tests and make monkey patching. 
We're managing this global state - we create a session on demand, only when it is needed.

## Factories
But `application` is still global and it is initialized on import. If we will not initialize the DB before running the tests it wouldn’t work. To address this problem the application factory pattern exists. The basic idea is to isolate `application` instance creation in a separate function. There are a few benefits of doing that:

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
- It is available as a fixture, which gives more flexibility (e.g. parametrization)

## Running speed vs test isolation
We fixed the global state on the Python level, but the database itself is a shared resource. 
It should be in the same state before each test run.

There are a couple of ways of doing this:
- Creating DB for each test case (slow/isolated)
- Recreate all tables & stuff for each test case (faster / less isolated)
- Wrap each test case in a transaction and rollback it at the end of a test case (fastest, even less isolated)

Each approach has its own pros and cons, but the main trade-off is speed vs test isolation. To be completely sure, that
each test case is isolated you can create a new database for each test case, but it will be very slow.
You can recreate all the tables for each test case, it will be faster, but you'll have to take care about re-creating stuff
you need for the tests - views/triggers / etc, usually, it is pretty easy to do with migrations.
Or you could create a transaction for each test case and roll it back in the end - super fast, but what if you need to
test some logic, that involves transaction manipulations? For example, Django has `TransactionTestCase` and `TestCase`
for dealing with different situations. `TransactionTestCase` truncates all tables and `TestCase` rolls back
 a transaction.