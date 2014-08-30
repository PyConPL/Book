# Python Memory Workshop 
## Abstract
A short “hands on” workshop on Python memory management. This workshop will cover basics of CPython memory usage and show essential differences between cPython and other implementations. We will start with basics like objects and data structures representation. Then advanced memory management aspects, such as sharing, segmentation, preallocation or caching, will be discussed. Finally, memory profiling tools will be presented. 


## Introduction
Working with Python does not usually involve debugging memory problems: the interpreter takes care of allocating and releasing system memory and you get to enjoy working on real world issues.
But what if you encounter such problems? 


What if your program:
  * never releases memory,
  * allocates way to much memory,
  * or you suspect that it is memory inefficient ?


This workshop will introduce you to the basics of Python Memory model, following with more advanced topics. During this tutorial you may learn basic memory profiling and debugging tools. Some advanced (implementation depended) topics will be discussed.  


## Workshop topics
Workshop will be divided into various topics. Each topic will include series of practical exercises. 


### Basic memory model
This topic will cover most of the memory basics:
  * Basic objects memory representation - what is the actual size of basic types, how to check it, various types features
  * Differences in basic objects representations among various Python implementations - PyPy, Stackless Python, Jython
  * Different data representations and how they affect memory consumption - this will cover:
    * Old style classes, New style classes, New style classes with slots, Named tuples, tuples, lists and dictionaries


### Advanced memory topics
Here some advanced concepts will be introduced, like:
  *  Object and String interning - this will explain objects are preallocated and are shared instead of new allocation. And more importantly this also will cover what are the motivations of this approach.
  *  Mutable Containers Memory Allocation Strategy - this will explain basics of memory strategy for containers. Examples for lists and dictionaries will be provided.
  * Notes with examples on Python garbage collector, reference count and cycles.
  * Differences in garbage collector among various Python implementations - PyPy, Stackless Python, Jython


### Basic memory profiling and debugging tools 
This topic will be entirely divided to various Python memory debugging and profiling tools:
  * Memory usage monitoring tools, such as: psutil, memory_profiler, run_snake_run
  * Object reference counting investigation: objgraph
  * Python heap analysis: Meliae, Heapy                                                                     


### Cpython memory allocator introduction 
This topic will go down to the internals of Python memory management, this will cover very advanced topics:
  * Memory fixing techniques
  * Python memory fragmentation
  * mallloc replacement considerations
  * testing memory problems with CPython 3.4 custom memory allocator
