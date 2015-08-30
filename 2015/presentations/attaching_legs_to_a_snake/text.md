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

## Other solutions - or - you don't always need an extension module

## Basic anatomy of an extension

## Configuration and building

## Python C API

## Linking to a library

## Boost.Python

## References

## Threading

## Summary

