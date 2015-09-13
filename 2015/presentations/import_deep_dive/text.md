# Import Deep Dive Detours - Petr Viktorin

Python's `import` statement hides a lot of complexity.
You could talk about it for hours, and still not cover it all.

My talk should make you understand import machinery well enough that it will
make sense when you want to study it further.
It shows the typical case of loading a simple Python module (or package),
omitting the various customization hooks, and ignoring the
ever-present hacks for backward compatibility.

To summarize, the import machinery has two major parts: the *finder*
and the *loader*.
The finder receives a name, and finds a file with the corresponding code,
typically by looking for `<modulename>.py` in directories listed in `sys.path`.
Its output is a `ModuleSpec` object that contains, among other things,
`origin` (the name of the `.py` file to load) and a loader object.

The loader then takes the ModuleSpec, creates a module object, and executes
code in the `.py` file to add the module's function class objects.

There are two major complications:
First, modules are cached in `sys.modules`, so re-importing a module is little
more than a dict lookup.
Second, for submodules, the parent package is always loaded before the submodule.

When reasoning about module imports, it's useful to keep in mind the exact
order the loading and caching is done in. In simplified pseudocode,
the import machinery looks like this:

    import_module(name):
        sys.modules[name]? return it

        if importing a submodule:
            load parent module
            sys.modules[name]? return it
            path = parent.__path__
        else:
            path = sys.path

        spec = find_spec(name, path)
        load(spec)  # sets sys.modules[name]

        module = sys.modules[name]
        if importing a submodule:
            set module as attribute of parent
        return module

    find_spec(name, path):
        for finder in sys.meta_path:
            call its find_spec(name, path)
            return spec if successful

    PathFinder.find_spec(name, path):
        for directory in path:
            get sys.path_hooks entry
            call its find_spec(name)
            return spec if successful

    load(spec):
        module = spec.loader.create_module(spec)
        if module is None:
            module = types.ModuleType(spec.name)

        set initial module attributes
        sys.modules[spec.name] = module
        spec.loader.exec_module(module, spec)

Most commonly, you will need to think about this when you're debugging import
cycles - the case where module A imports module B, which in turn imports A
again. Import cycles are hard to get right, and perhaps even harder to keep
working as your code changes.
The best advice for import cycles is to get rid of them, typically by putting
common code in its own module.

For packages, the rule of thumb to avoid import-related trouble are:

* `__init__` should:
    * import from submodules
    * set `__all__`
    * nothing else
* submodules should:
    * not import directly from `__init__`
    * not have internal import cycles

Now, there are still some topics that I haven't covered in the 30 minutes
of my talk. This article dives into a few more tidbits and special cases related to
importing: namespace packages, real-world examples of projects that use custom
importers, Loader-assisted resource loading, the rules for C extension modules,
and more information on the `__main__` module.


## Namespace packages and plugin systems

Probably the most important omission in my talk are namespace packages.

When `PathFinder.find_spec` loops through the path entries, it looks for
either a file (which would become a module), or a directory with an
`__init__` file (which would become a package).

What I didn't tell you is that it actually looks for *all* directories,
even if they don't contain `__init__`. Any `__init__`-less directories
are remembered for later.

If the finder finishes going through `path` without finding a suitable module,
it makes a *namespace package*: an empty module whose `__path__` contains all
the directories remembered.

But why do that?

Namespace packages are usually used to implement plugin systems.
Suppose there is an extensible sound editor, where individual filters
(like "echo", "reverb" and "speedup") are implemented as Python modules,
and can be installed individually.

"Individually" means "in different locations".
Your `sys.path` will usually include several kinds of locations. On a Linux
machine, the path will typically have:

* Directories from `$PYTHONPATH`, and the current directory
* The Python standard library (e.g. `/usr/lib/python3.4`)
* User-specific locations (e.g. `~/.local/lib/python3.4/site-packages`)
* A place for system-wide installed packages (e.g. `/usr/lib/python3.4/site-packages`)

Suppose you install the editor and a built-in "echo" filter system-wide,
a private "reverb" filter to your home directory, and you have "speedup"
(which you're currently developing) in the current directory (on `$PYTHONPATH`).
The paths to these modules would be:

* /usr/lib/python3.4/site-packages/sound_editor_filters/echo.py
* ~/.local/lib/python3.4/site-packages/sound_editor_filters/reverb.py
* ./sound_editor_filters/speedup.py

And that repeated `sound_editor_filters` directory becomes a namespace package:

    >>> import sound_editor_filters
    >>> sound_editor_filters.__path__
    _NamespacePath([
        './sound_editor_filters',
        '~/.local/lib/python3.4/site-packages/sound_editor_filters',
        '/usr/lib/python3.4/site-packages/sound_editor_filters'])

Importing `sound_editor_filters.echo` will get you the correct module,
because submodules are searched for in the `__path__` of their parent.

Remember that adding an `__init__.py` to *any* of the `sound_editor_filters`
directories will cancel the magic. Any directory with `__init__` is a regular
package, its `__init__`-less siblings are ignored.

Long before namespace packages were added to CPython, `setuptools` contained
[an utility](https://pythonhosted.org/setuptools/setuptools.html#namespace-packages)
to declare namespaces manually and explicitly.
Of course, this still works - and if you need to support Python 2,
it's the way to go.


## Customization examples

Another topic that didn't make it to my talk is customization:
how to extend importlib to do new, exciting things?

If you're interested in this, I'll just direct you to
[importlib documentation](https://docs.python.org/3/library/importlib.html).
Now that you know the terminology and the "normal" way of how things are
done, those docs should make much more sense.

Instead, I'll mention some real-world projects that use custom import hooks,
which you can use as an inspiration about what's possible.

Hy (hy.readthedocs.org) allows you to import modules written in a dialect of
Lisp. Or as its docs put it, it's "lisp-stick on a Python".
It uses a custom finder that looks for `*.hy` files instead of `*.py` ones,
and a corresponding loader that parses the Lisp code, runs it, and populates
a Python module object with the resulting functions and objects.

This is a good approach for any project that wants to embed a custom language
in the Python runtime.

The Macropy project uses a similar technique to add syntactic macros to
Python code. Conceptually, it's the same as Hy, except that the language is a bit
more similar to Python.

Perhaps most widely used of import customizations is Cython's `pyximport`,
which finds a `.pyx` file, compiles it into a C extension, and then imports it.

If you just want to load Python modules that are stored in a non-standard
location, like a database, Git repository, or just a string,
look near the end of David Beazley's PyCon US 2015 tutorial for his
Redis importer.


## Loading Module Resources

Every module uses a `Loader` object when it is first initialized, but the
usefulness of loaders doesn't end there.

Loaders of most types of modules implement the `ResourceLoader` ABC, a protocol
that allows loading data files stored alongside a module.
For example, to open a data file stored "next to" the current module on the
filesystem, a common approach is to do:

    >>> import os
    >>> filename = os.path.join(os.path.dirname(__file__), "file.dat")
    >>> with open(filename, 'rb') as f:
    ...     data = f.read()

However, this will only work when the module and data are loaded from regular
files. If they were, for example, distributed in a zip file, the `open`
function would fail.

A more robust approach is to do:

    >>> import os
    >>> filename = os.path.join(os.path.dirname(__file__), "file.dat")
    >>> data = __loader__.get_data(filename)

While constructing the filename is still somewhat painful, this approach will
work with zipped packages, and any other loaders that implement `get_data`.

(Sadly, David Beazley's Redis importer does not support this yet.)


## Extension and built-in modules

A big part of CPython's appeal (especially back when it was just starting) is
that it is easily extensible with code written in C, so you can interface with
existing libraries or write code that runs fast.
Today, it's generally better to use CFFI or Cython for this, but extensions
remain important. If nothing else, a big part of the the standard library
is written in C.
(And CPython extensions don't need to be written in C -
any language that can export C-like functions, such as
C++ or Rust, will do.) Anyway, how are extension modules loaded?

An extension is a shared library, such as a DLL on Windows or a `.so` file on
Linux. It exports one function called `PyInit_<modulename>`.

When the shared library file is found (using `PathFinder` as normal),
an ExtensionFileLoader is created to handle the loading.

The difference from Python modules is in the loader's methods.
Step one: `create_module` loads the shared library and calls `PyInit_<modulename>`.
PyInit is – for historical reasons – responsible for both creating the module
object and initializing it. So, there's no step two:
`ExtensionFileLoader.exec_module` does nothing.

PyInit is called without any arguments, so it doesn't have access to the
`ModuleSpec` and the things it includes, like the filesystem path of our
module. This makes loading data from related files quite tricky.
Also, calling user-written code from the PyInit function is somewhat
dangerous, because `sys.modules` is not updated until after the initialization
is done.
To overcome these problems, there's a new mechanism in Python 3.5,
which allows extensions to customize both the `create_module` and
`exec_module` steps. It's called "multi-phase initialization", and
it's explained in PEP 489.

Built-in modules, like `io` or `zipimport`, are very similar to extension
modules. Pretty much the only difference is the loading step: they're looked up
in a compiled-in list rather than found in the filesystem.
If you embed Python, or build it from source, you can add your own
PyInit functions to this list.


## The special snowflake: `__main__`

The `__main__` module is quite special.

The `loader.create_module` step for it is done very early during
interpreter startup - so early that the import machinery isn't loaded yet.
The module object is created directly, and remembered deep in C code.

When the time comes to run some code - the file Python was given to
interpret, or a module given with the `-m` switch, or even commands from
interactive console - it is executed inside `__main__`'s namespace.

Python has an `-i` command-line switch, which causes it to drop to interactive
prompt after running code. If you invoke:

    $ python3 -i somemodule.py

the contents of `somemodule.py` are run inside the `__main__` module.
When it's done, you're given a chance to give commands, which are also
executed in the `__main__` namespace. So, if the module defined some functions,
you're able to use them right away.

The mechanism for doing this assumes that the `__main__` module object is the
same as the one created during early initialization. This has some implications
for the types of modules Python can run directly. As explained in the previous
section, traditional C extensions implement all of `loader.create_module` on
their own, so they can't use the pre-existing `__main__`.
Sure enough, when you invoke `python -m math`, you just get an error.
(As for PEP 489 extension modules: it would be theoretically possible to run
some of these directly, and hopefully the support will be added in Python 3.6)

However, Python can run *packages* directly.
It doesn't run the `__init__.py` when you ask to run a package. That would
encourage people to violate our rules of what goes in `__init__`.
(Remember: import from subpackages, set `__path__`, nothing else. Especially
not a big `if __name__ == "__main__"` block.)
Rather, a submodule named `__main__` is executed.

You can run a number of package-like things:

* `$ python -m somepackage`  (when the package has a `__main__` subpackage)
* `$ python some-directory/`  (when the directory has a `__main__.py` file)
* `$ python archive.zip`  (when the archive includes a `__main__.py` file)

In fact, when you see a file with a `.pyz` extension, it's nothing more than
a Python module with a `__main__.py`, bundled in a zip archive.
You can run these directly – on Unix, they need a correct shebang;
on Windows they need a correct extension.
In Python 3.5, the `zipapp` tool can produce such executable archives for you,
but the support for running them has been there since Python 2.6.


## References

The documentation of the import machinery's is abundant (if somewhat perplexing
for the uninitiated).
You should definitely read the importlib documentation:

* https://docs.python.org/3/library/importlib.html

or watch David Beazley's fun-filled tutorial:

* "Modules and Packages: Live and Let Die!" (PyCon 2015): http://pyvideo.org/video/3387

and talks by Bret Cannon, the author of importlib:

* "How Import Works" (PyCon 2013): http://pyvideo.org/video/1707
* "Import this, that, and the other thing" (PyCon 2010): http://pyvideo.org/video/341

For interesting detours and change summaries, look no further than the related PEPs:

* PEP 328 – Imports: Multi-Line and Absolute/Relative
* PEP 3147 – PYC Repository Directories
* PEP 302 – New Import Hooks
* PEP 451 – A ModuleSpec Type for the Import System
* PEP 420 – Implicit Namespace Packages
* PEP 441 – Improving Python ZIP Application Support
* PEP 338 – Executing modules as scripts
* PEP 3149 – ABI version tagged .so files
* PEP 489 – Multi-phase extension module initialization
* PEP 235 – Import on Case-Insensitive Platforms
* PEP 263 – Defining Python Source Code Encodings
* PEP 3120 – Using UTF-8 as the default source encoding

And lastly, for the true deep dive, peek in the importlib sources:

* https://hg.python.org/cpython/file/3.5/Lib/importlib

If anything is unclear, ask! That's what I did :)

Many thanks to Nick Coghlan, Brett Canon, Eric Snow, Stefan Behnel and everyone
else involved with PEP 489 discussions, which forced me to learn all this.
