# Attaching legs to a snake - or - Python3 extensions - Tomasz Maćkowiak

## Introduction

Python is a powerful language by itself. The robust standard library and the myriad of additional packages make it a Swiss Army knife of programming languages. But sometimes it is not enough. When you need to integrate with a low-level C API or execute heavy computations without the interpreter overhead, writing a Python extension module might be a good idea.

This artice will show you how to write, build and run an extension; what C API you can use in it and what to remember about; how to link to shared libraries and what does Boost.Python simplify.

## Overview of the extension's anatomy

### Head

As any code written in C, Python extensions must load the appropriate header file to let the compiler know what functions of the Python C API are available.
We usually only need to include one file:
```
#include <Python.h>
```

### Body

Most Python function are taking ```PyObject``` pointer argument (sometimes more of them) and are returning a ```PyObject``` pointer. This is the Python's *everything is an object* put into practice.
```
static PyObject *
basic_hello(PyObject *self)
{
    const char * msg = "Hello world";
    return PyUnicode_FromString(msg);
}
```
In case of this module-level function, ```self``` parameter will be the reference to the extension module the function if attached to.

### Limbs

We need to declare what functions our module exposes. We declare the name under which the function will be visible, the pointer to the function itself, type of arguments it expects (no arguments, positional arguments or keyword arguments) and a docstring:
```
static PyMethodDef basic_methods[] = {
    {"hello", (PyCFunction)basic_hello, METH_NOARGS, "Return hello world."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
```

### Nervous system

We need to define the module itself: it's name, docstring, optional size of the module-state, function definitions:
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

### Hearth

The most important though is the module initialisation function that creates module based on the module definition:
```
PyMODINIT_FUNC
PyInit_basic(void)
{
    return PyModule_Create(&basic_module);
}
```

## Animation - how to make it come alive

The extensions are easy to build (on most platforms). One needs a compiler and Python development libraries:
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
As you can see there are no special commands needed for installing packages that have C extension modules. The extensions are automatically build even if your package is just a dependency of another Python package.

## Digestive system - parsing parameters

### Positional parameters

To parse position parameter you need to define your function with ```METH_VARARGS``` flag in the module's function declarations:
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
The description of the formatting parameters can be found in the docs. ```s``` means *convert to C string* (```char *```). ```I``` means convert to ```unsigned```. ```O``` would mean pass a Python object and the parameter could be placed into a ```PyObject *``` variable.

Notice that you are passing addresses of the variables (using the ```&``` operator) - this is what enables Python to write the values into your variables in a return-parameter manner.

### Keywords parameters

If you want to give your users more freedom in passing parameters to your extension function, you can use keyword parameters. You need to declare the appropriate flag for your function:
```
{"belongs",  (PyCFunction)key_belongs, METH_VARARGS | METH_KEYWORDS, "..."},
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

Most of Python API functions can indicate a failure. If the function is supposed to return a ```PyObject *```, it will return ```NULL``` when it fails. The details of the exception are set in the per-thread interpreter state. If we detect an failed function call, we can just return the same ```NULL``` from our function. The details of the original exception are still stored within the interpreter, so if we don't modify the exception state, the original exception will be used. For example the ```PyArg_ParseTuple``` function can return ```NULL``` if you pass an ```int``` where you were supposed to pass a ```str```. It will set the exception state to a ```TypError``` with message ```'must be str, not int'```. We can also set our own exception:
```
PyErr_SetString(PyExc_RuntimeError, "Cannot format output");
return NULL;
```

Some functions (for example ```__init__``` C implementation) are supposed to return an ```int``` status. To signal an encountered exception set the exception info using ```PyErr_SetString``` (or leave the one already set if the exception is coming from a deeper Python function call) and return ```-1``` from your function.

## API

The API you can use in your Python C extensions if quite vast. You can read all about it in the Python docs. API is split into section, so all functions dealing with ```str``` are in one section (funny fact: in the API ```str``` is still refered to as ```Unicode```, for example ```PyUnicode_FromString```), etc. You can find the equivalent calls for your Python constructs. Here are some examples:

To get a item under given key in a dictionary (```category_sequence = mapping[category]```) use:
```
/* GetItem returns a new reference that needs to be decremented */
PyObject * category_sequence = PyObject_GetItem(mapping, category);
if (category_sequence == NULL) {
    return NULL;
}
// Deal with the object ...
Py_DECREF(category_sequence);
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

## Population size

Python automatically manages memory using **reference counting** and a cyclic garbage collector. Reference counting means that for each Python object (```PyObject```) the interpreter stores a count of how many other object are referencing it. Say you have two dictionaries:
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

Knowing when to increase ref. count and when to decrease it is one of the hardest things to get right. When using any Python API function we need to read if it returns *new reference* or *borrowed reference*. The former means that the object returned by the API function already has the reference count increased, so we need to decrease it when we are done dealing with it. In the latter case the reference count was not increased - our code didn't become one of the owner's of the object's reference, so there is no need to decrease it when we are done dealing with it. But if we would like to return it from our function or store it, we need to increase the reference count to make sure that Python will not deallocate that object.

Check out the example of dealing with references:
```
PyObject * mapping = ...;
PyObject * item = ...;
PyObject * category = ...;

/* GetItem returns a new reference that needs to be decremented */
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

## Objects

## GIL and threading

## Boost

## References

## Summary

