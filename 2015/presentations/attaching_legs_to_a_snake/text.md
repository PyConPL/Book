# Attaching legs to a snake - or - Python3 extensions - Tomasz Maćkowiak

## Introduction

Python is a powerful language by itself. The robust standard library and the myriad of additional packages make it a Swiss Army knife of programming languages. But sometimes it is not enough. When you need to integrate with a low-level C API or execute heavy computations without the interpreter overhead, writing a Python extension module might be a good idea.

This artice will show you how to write, build and run an extension; what C API you can use in it and what to remember about; how to link to shared libraries and what does Boost.Python simplify.

Full source codes for all example modules below can be found on github [1].

## Overview of the extension's anatomy

### Head

As any code written in C, Python extensions must load the appropriate header file to let the compiler know what functions of the Python C API are available.
We usually only need to include one file:
```
#include <Python.h>
```

### Body

Most Python function are taking ```PyObject``` pointer argument (sometimes more of them) and are returning a ```PyObject``` pointer. This is Python's *everything is an object* put into practice.
```
static PyObject *
basic_hello(PyObject *self)
{
    const char * msg = "Hello world";
    return PyUnicode_FromString(msg);
}
```
In case of this module-level function, ```self``` parameter will be the reference to the extension module the function is attached to.

### Limbs

We need to declare what functions our module exposes: 
```
static PyMethodDef basic_methods[] = {
    {"hello", (PyCFunction)basic_hello, METH_NOARGS, "Return hello world."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
```
We declare the name under which the function will be visible, the pointer to the function itself, type of arguments it expects (no arguments, positional arguments or keyword arguments) and a docstring.

### Nervous system

We need to define the module itself:
```
static struct PyModuleDef basic_module = {
   PyModuleDef_HEAD_INIT,
   "basic",   /* name of module */
   "The simplest module", /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   basic_methods
};
```
 We pass it's name, docstring, size of the optional module state memory block and function definitions.

### Hearth

The most important though is the module initialisation function that creates the module based on the module definition:
```
PyMODINIT_FUNC
PyInit_basic(void)
{
    return PyModule_Create(&basic_module);
}
```

## Animation - how to make it come alive

The extensions are easy to build (on most platforms). One needs a compiler and Python development library:
```
sudo apt-get install python3-dev build-essential
```
or equivalent command for your system.

Extensions are declared in the ```setup.py``` file of your package:
```
from setuptools import find_packages, setup, Extension

basic = Extension('basic', sources=['src/basic_mod/basic.c'])

setup(
    name='pyext',
    version='0.1',
    ext_modules=[basic],
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
```
Once you have this, you can build your extension using
```
python3 setup.py build
```
If you want to install it into your system or virtualenv, execute
```
python3 setup.py install
```
As you can see there are no special commands needed for installing packages that have C extension modules. The extensions are automatically built even if your package is just a dependency of another Python package.

## Digestive system - parsing parameters

### Positional parameters

To parse positional parameters you need to define your function with ```METH_VARARGS``` flag in the module's functions declaration:
```
{"hello",  param_hello, METH_VARARGS, "Say hello."},
```
With such declaration your function will get one more parameter, similar to ```*args``` construct in pure Python:
```
static PyObject *
param_hello(PyObject *self, PyObject * args) {
    ...
```
To parse the incoming parameters you can use the ```PyArg_ParseTuple``` function. You pass into the function the incoming arguments object, format string specifying what arguments you expect and a set of pointers where the data parsed from the parameters should be inserted. Before you call ```PyArg_ParseTuple``` you need to allocate space for the variables the parameters will be placed into:
```
const char * name;
unsigned age;
```
Only then you can attempt to parse parameters:
```
if (!PyArg_ParseTuple(args, "sI", &name, &age)) {
    return NULL;
}
// Parameters parsed, carry on ...
```
The description of the formatting parameters can be found in the docs [2]. ```s``` means *convert to C string* (```char *```). ```I``` means convert to ```unsigned```. ```O``` would mean pass a Python object and the parameter could be placed into a ```PyObject *``` variable.

Notice that you are passing addresses of the variables (using the ```&``` operator) - this is what enables Python to write the values into your variables in a return-parameter manner.

### Keyword parameters

If you want to give your users more freedom in passing parameters to your extension function, you can use keyword parameters. You need to declare the appropriate flag for your function:
```
{"belongs", (PyCFunction)key_belongs, METH_VARARGS | METH_KEYWORDS, "..."},
```
thus making Python pass it one more ```PyObject *```:
```
static PyObject *
key_belongs(PyObject *self, PyObject * args, PyObject * kwargs) {
    ...
```
You need to define the names of the incoming parameters:
```
static char * keywords[] = {"mapping", "item", "category", NULL};
```
and then you can use ```PyArg_ParseTupleAndKeywords``` function passing it both positional and keyword arguments:
```
if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO", keywords, &mapping, &item, &category)) {
    return NULL;
}
// Carry on ...
```

## Hiccups - exceptions

Most of Python API functions can indicate a failure. If the function is supposed to return a ```PyObject *```, it will return ```NULL``` when it fails. The details of the exception are set in the per-thread interpreter state.

If we detect an failed function call, we can just return the same ```NULL``` from our function. The details of the original exception are still stored within the interpreter, so if we don't modify the exception state, the original exception will be used.

For example the ```PyArg_ParseTuple``` function can return ```NULL``` if you pass an ```int``` where you were supposed to pass a ```str```. It will set the exception state to a ```TypError``` with message ```'must be str, not int'```. We can also set our own exception:
```
PyErr_SetString(PyExc_RuntimeError, "Cannot format output");
return NULL;
```

Some functions (for example ```__init__``` C implementation) are supposed to return an ```int``` status. To signal an encountered exception set the exception info using ```PyErr_SetString``` (or leave the one already set if the exception is coming from a deeper Python function call) and return ```-1``` from your function.

## Bones - API

The API you can use in your Python C extensions if quite vast. You can read all about it in the Python docs [2]. API is split into sections, so all functions dealing with ```str``` are in one section (funny fact: in the API ```str``` is still refered to as ```Unicode```, for example ```PyUnicode_FromString```), etc. You can find the equivalent calls for your Python constructs. Here are some examples:

To get an item under given key in a dictionary (```category_sequence = mapping[category]```) use:
```
PyObject * category_sequence = PyObject_GetItem(mapping, category);
if (category_sequence == NULL) {
    return NULL;
}
// Deal with the object ...
```

To check if a sequence contains given item (```contains = item in category_sequence```) use:
```
int contains = PySequence_Contains(category_sequence, item);
if (contains == -1) {
    return NULL; // error, for example KeyError
} elif (contains == 0) {
    ... // doesn't contain
} else {
    ... // does contain
}
```

## Population size - reference counting

Python automatically manages memory using **reference counting** and a cyclic garbage collector. Reference counting means that for each Python object (```PyObject```) the interpreter stores a count of how many other objects are referencing it. Say you have two dictionaries:
```
dict_a = {'a': 'VALUE'}
dict_b = {}
```
The ```str``` object ```'VALUE'``` has reference count of ```1``` - only the object ```dict_a``` is referencing it. Once we do:
```
dict_b['b'] = dict['a']
```
then our ```str``` object is referenced by both ```dict_a``` and ```dict_b``` so it's reference count is raising to ```2```. If we remove both references:
```
del dict_a['a']
del dict_b['b']
```
then our ```str``` is no longer referenced by anything, it's reference count drops to ```0``` and the interpreter knows that this object is no longer used, so the memory it occupied can be freed and later on reused.

This process of counting references is happening automatically in pure Python, but requires manual support when dealing with Python objects in C extensions.

We need to manually increase the reference count on an object using
```
Py_INCREF(result);
```
and decrease it using
```
Py_DECREF(category_sequence);
```
macros.

Knowing when to increase ref. count and when to decrease it is one of the hardest things to get right. When using any Python API function we need to read if it returns *new reference* or *borrowed reference*.

The former means that the object returned by the API function already has the reference count increased, so we need to decrease it when we are done dealing with it.

In the latter case the reference count was not increased - our code didn't become one of the owners of the object's reference, so there is no need to decrease it when we are done dealing with it. But if we would like to return it from our function or store it, we need to increase the reference count to make sure that Python will not deallocate that object.

Check out the example of dealing with references:
```
PyObject * mapping = ...;
PyObject * item = ...;
PyObject * category = ...;

/* GetItem returns a new reference so the object's ref. count needs to be decremented */
PyObject * category_sequence = PyObject_GetItem(mapping, category);
if (category_sequence == NULL) {
    return NULL;
}

int contains = PySequence_Contains(category_sequence, item);
Py_DECREF(category_sequence); // We will no longer need this object.
if (contains == -1) {
    return NULL;
}

PyObject * result = contains ? Py_True : Py_False;
// True and False are singleton-like objects, if we want to return them
// from our code, we need to increase their ref. count
Py_INCREF(result);

return result;
```

## Species - classes

It is possible to have classes implemented in C. It requires extending the code of your extension module with additional elements.

An additional header needs to be included:
```
#include <structmember.h>
```

Then the structure (fields) of the class objects needs to be defined:
```
typedef struct {
    PyObject_HEAD // Required header fields
    char * pointer;
    long number;
    PyObject * name;
} Native;
```
The structure needs to start with the required fields from ```PyObject_HEAD``` macro, but the the rest of the members can be defined freely by the developer.
The fields can reference other Python objects (```PyObject *```), can be primitive types (```long```), pointers (```char *```) or any other type, even if Python will not be able to apply any default conversion to it.

Once we define the structure, we can also define a Python mapping of fields, so that we will be able to access them straight from Python (```obj = Native(...); obj.name```):
```
static PyMemberDef Native_members[] = {
    {"name", T_OBJECT_EX, offsetof(Native, name), 0, "Name"},
    {"number", T_LONG, offsetof(Native, number), 0, "Number"},
    {"pointer", T_STRING, offsetof(Native, pointer), READONLY, "Pointer"},
    {NULL}  /* Sentinel */
};
```
For each member we define a name, type, offset in class structure, flags and a docstring.

We can also define what methods will be available on our objects:
```
static PyMethodDef Native_methods[] = {
    {"summary", (PyCFunction)Native_summary, METH_NOARGS, "Return the name and the other attributes formatted"},
    {NULL}  /* Sentinel */
};
```

The methods will be receiving a pointer to a ```Native``` instance as first parameter:
```
static PyObject *
Native_summary(Native* self)
{
    if (self->name == NULL) {
        PyErr_SetString(PyExc_AttributeError, "name");
        return NULL;
    }

    return PyUnicode_FromFormat(
        "Native %S number %li pointer %s",
        self->name, self->number, self->pointer
    );
}
```

The most important bit is the class definition:
```
static PyTypeObject NativeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "obj.Native",              /* tp_name */
    sizeof(Native),            /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Native_dealloc,/* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "Native objects",          /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    Native_methods,            /* tp_methods */
    Native_members,            /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Native_init,     /* tp_init */
    0,                         /* tp_alloc */
    Native_new,                /* tp_new */
};
```
In this structure we can define some of the special functions that we implement for our type. Most common ones would be implementing ```__new__```, ```__init__``` and object deallocation.

A sample ```__new__``` implementation:
```
static PyObject *
Native_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    Native *self;
    /* Call the base allocator */
    self = (Native *)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL; // Failed to allocate.
    }
    self->number = 0;
    self->name = PyUnicode_FromString("");
    if (self->name == NULL) {
        Py_DECREF(self);
        return NULL;
    }
    self->number = 0;
    self->pointer = (char *)malloc(sizeof(char) * 4);
    if (self->pointer == NULL) {
        Py_DECREF(self->name);
        Py_DECREF(self);
        return PyErr_NoMemory();
    }
    strcpy(self->pointer, "?");

    return (PyObject *)self;
}
```

A sample ```__init__``` implementation:
```
static int
Native_init(Native *self, PyObject *args, PyObject *kwargs)
{
    PyObject * name = NULL;
    PyObject * tmp;
    int yes_no;

    static char *kwlist[] = {"name", "number", "yes", NULL};

    if (!PyArg_ParseTupleAndKeywords( // l = long, p = boolean evaluation
        args, kwargs, "Olp", kwlist, &name, &self->number, &yes_no
    )) {
        return -1;
    }

    if (name) {
        tmp = self->name;
        Py_INCREF(name);
        self->name = name;
        Py_XDECREF(tmp);
    }

    strcpy(self->pointer, yes_no ? "YES" : "NO");

    return 0;
}
```
Notice how this function returns an ```int``` - ```__init__``` cannot return any other object but is used to initialize the ```self``` object.

Sample deallocation implementation:
```
static void
Native_dealloc(Native * self)
{
    Py_XDECREF(self->name);
    if (self->pointer != NULL) {
        free(self->pointer);
    }
    Py_TYPE(self)->tp_free((PyObject *)self);
}
```

The last thing that remains is to initialize and connect our type when module loads:
```
PyMODINIT_FUNC
PyInit_obj(void)
{
    PyObject * module;

    if (PyType_Ready(&NativeType) < 0) {
        return NULL;
    }

    module = PyModule_Create(&obj_module);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&NativeType);
    PyModule_AddObject(module, "Native", (PyObject *)&NativeType);

    return module;
}
```

## GIL and threading
Python has the Global Interpreter Lock - only one thread at a time can be executing Python code. This property of the language is making it better for multi-process setups than multi-thread setups. But inside the code of our extension module we can declare a block as not-using-Python - not executing **any** Python API functions and not operating on any Python structures passed to it as arguments etc. Such code can be executed *while* some other tread *is* executing different Python code **at the same time**. We should be releasing the interpreter whenever a blocking operation is being executed as long as it doesn't use any Python structures.

Here is an example of how to wrap computations so they don't hold the interpreter and so that they can be executed in threads in paralell with other Python code:
```
static PyObject *
gil_calc_release(PyObject * self, PyObject * args)
{
    long n;
    if (!PyArg_ParseTuple(args, "l", &n)) {
        return NULL;
    }
    long result;

    Py_BEGIN_ALLOW_THREADS
    result = fibonacci(n);
    Py_END_ALLOW_THREADS

    return PyLong_FromLong(result);
}
```

## Boost
A popular C++ library *Boost* provides the *Boost.Python* module for easier writing of Python extensions in C++.

### C++ code

With *Boost* a different header is used:
```
#include <boost/python.hpp>

using namespace boost::python;
```

Functions can be declared with C++ arguments that will be automatically parsed by *Boost.Python*:
```
bool has_letter(const char * text, const char letter) {
    const char * ptr = text;
    while (char c = *(ptr++)) {
        if (c == letter) {
            return true;
        }
    }
    return false;
}
```

To register such a function we don't need to create a module definition or module members structure, all we need is the module initialization function:
```
BOOST_PYTHON_MODULE(boost)
{
    def("has_letter", has_letter);
}
```

Extensions written using *Boost.Python* can be much more concise.

### Compiling

*Boost.Python* comes as a shared library. That means that during compilation and executing of our extension Python needs to be able to read the library's files. If the library is installed system-wide, you don't have to worry about paths. If the library is installed locally, you need to remember to pass the correct includes path and library path during compilation and to have the ```LD_LIBRARY_PATH``` system variable correctly set during running.

The ```setup.py``` for a *Boost.Python* extension can look like this:
```
boost = Extension(
    'boost',
    sources=['src/boost_mod/boost.cpp'],
    include_dirs=[os.path.join(BOOST_DIR, 'include')],
    libraries=["boost_python"],
    library_dirs=[os.path.join(BOOST_DIR, 'lib')],
)
```
Notice that we specify here that our extension should be linked to the ```boost_python``` shared library.

*Boost.Python* also allows you to define classes in a simplified syntax.
```
struct Native
{
    std::string name;
    long number;
    std::string pointer;

    Native(std::string name, long number, bool yes): name(name), number(number) {
        this->pointer = std::string(yes ? "YES" : "NO");
    }

    std::string summary() {
        std::stringstream ss;
        ss << "Native " << this->name << " number " << this->number << " pointer " << pointer;
        return ss.str();
    }
};

BOOST_PYTHON_MODULE(boost)
{
    class_<Native>("Native", init<std::string, long, bool>())
        .def_readwrite("name", &Native::name)
        .def_readwrite("number", &Native::number)
        .def_readonly("pointer", &Native::pointer)
        .def("summary", &Native::summary);
}
```

## Summary

Python extensions are a great tool for pushing the boundaries of what Python can do. Whether we want to code some calculations to work faster without the interpreter's overhead of if we want to integrate with a shared library, extensions provide us a way of doing it while still keeping the usual package installation procedure.

Extensions are powerful and you can implement some really cool stuff with them [3], but you need to be very careful. Dealing with low level C is dangerous on it's own and dealing with Python's internals at the same time is adding to the complexity. One ```PyDECREF``` missing and you will have memory leaks, one ```PyDECREF``` too many and your extension will crash the whole interpreter with a core dump. Good luck!

## References

* [1] [GitHub repo with full source code of all examples](https://github.com/kurazu/pyext)
* [2] [Python/C API Reference Manual](https://docs.python.org/3/c-api/index.html)
* [3] [GitHub repo of a Python-SpiderMonkey integration library](https://github.com/kurazu/bridge)

