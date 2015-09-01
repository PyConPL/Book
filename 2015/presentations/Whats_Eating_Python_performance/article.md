#  What's Eating Python performance - Piotr Przymus
Have you ever wondered how to speed up your code in Python? This presentation will show you how to start. I will begin with a guide how to locate performance bottlenecks and then give you some tips how to speed up your code. Also I would like to discuss how to avoid premature optimisation as it may be ‘the root of all evil’ (at least according to D. Knuth). 

## Introduction

Code optimisation is an important aspect of development process, but when done improperly it may do more harm than good.
This talk is intended as a gentle introduction into good practices in Python code optimisation. 
Certainly this does not exhaust the topic, and there are various great resources where you can find more on Python optimisation, see references for some starting points.

This talk mainly focuses on CPython (both >= 2.7 and >= 3.4) Python implementation.

## Improving the performance: overview

### The root of all evil: premature optimisation 

*Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: premature optimisation is the root of all evil. ~ *
**Donald Knuth**, "Structured Programming With Go To Statements".

In short premature optimisation may be stated as optimising code before knowing that we need to. 
This may be a dangerous practice that will impact on your productivity, readability of the code and ease of maintenance and debugging
(it also may contradict many points of The Zen of Python).

So it is important to learn how to do proper assessment of your code in terms of optimisation needs. 
(Remember that strong felling that your code falls into the remaining 3% does not count!)

Yet do not be discouraged from learning the proper way of optimising your code, and remember about second part of the previous quote:

*Yet we should not pass up our opportunities in that critical 3%.* **Donald Knuth**

It also worth noting, that certain optimisations are part of good programming style and good practices, and therefore should not be considered as premature.
For example moving computations that do not depend on the loop, outside the loop, as this also improve code readability.

#### Think before doing (Think before coding)

Going for higher performance without a deeper reason may be just a waste of your time.
So start with:

  * stating your reasons (Why do you need higher performance ?),
  * defining your goals (What would be an acceptable speed of your code?),
  * estimating time and resources you are willing to spend to achieve defined goals.

Re-evaluate all the pros and cons.

## Test, Measure, Track Down bottlenecks, Fix

A starting point for optimisation is a running code which gives correct results. 
Having that you should prepare a regression test suite, which will stand on guard of the correctness of your code during the optimisation.

Then rest of the optimisation process may be summarized as: 
 
  1. Test if the code works correctly.
  2. Measure execution time and if code is not fast enough use profiler to identify the bottlenecks.
  3. Optimise.
  4. Start from the beginning.

### Regression test suite

Before you start it is crucial to prepare regression test suite that is comprehensive but yet quick-to-run.
As test will be ran very often it is important that it will run in a reasonably amount of time.
Consider, breaking the tests into fast and slow categories, if running full test suite takes too much time.

### Measuring execution time and tracking down the bottlenecks: Measuring and profiling tools 

Next, you should measure execution time of your code. 
This is important because:

  * it allows you to check how does current execution time relates to desired execution time (i.e. acceptable speed),
  * secondly, it allows you to compare various version of optimisations in code.

There are various tools to do that, among them:

  * Pythons timeit module,
  * custom made timer using Pythons time module,
  * unix time (use /usr/bin/time as time is also a common shell built in).

Notes on measuring:

  * Try to measure multiple independent repetitions of your code (this will help you to establish the lower bound of your execution time).
  * Prepare a testing environment that will allow you to get comparable results.
  * Consider writing a micro benchmark to check various alternative solutions of some algorithm.
  * Be careful when measuring algorithm speed using artificial data, re-validate using real data.


Profiling tools will give you a more in depth view of your code performance.
This will allow you to take a view of your program internals in terms of execution time and used memory.

There are various possible tools, like:

  * cProfile - a profiling module available in Python standard library,
  * line\_profiler - an external line-by line profiler,
  * tools for visualizing profiling results - for example, runsnakerun.

#### IO bound vs compute bound
It is important that you learn how to classify types of performance bounds of your code.
**The compute bound** case occurs when large number of instructions is making your code slow, the **I/O bound** case takes place when your code is slow because of various I/O operations, like network  delays or disk access.  
Depending on the type of the performance bound, different optimisation strategies will apply.

### Fixing the cause: Performance Tips

#### Algorithms and data structures

Improving your algorithms time complexity is probably the best thing that you could do to optimise your code.
Using micro optimisation tricks will not bring you any wear near to the speed boost you could get from improving time complexity of algorithm.

It is very common that innocently looking searching or lookup code placed in a large loop generates a performance issue.
Often a trivial change, like changing list to set, may be a key to solving the problem.

That said be sure to check page [Time complexity](https://wiki.python.org/moin/TimeComplexity) from Python's wiki and confront it with data structures used in your algorithms.  
The big **O** notation matters!

#### Improving the code work flow

Often you may encounter a loop, with code that performs expensive time/memory computations that do not change within loop.
Fix it by moving those operations outside a loop (just before the loop start). 
Beware that such operations may be hidden in a class method or in a free function.

Try to avoid conditional branching in large loops. 
Check whatever instead of having if/else statements in the loop body:

  * is it possible to do the conditional check outside the loop
  * or have separate loops for different branches.

Python introduces relatively high overhead for function/method calls. 
In some cases it may be worth to consider code inlining to avoid the overhead. 
But this comes at cost of code maintenance and readability.

There are also other techniques, like improving function/method/variable/attribute lookup times or loop unrolling.

#### Memory and I/O bounds 

Some performance issues may be memory related, so checking memory utilization is also a good idea.
Typical symptoms that indicate that your code may have memory problems:

  * your program never releases memory,
  * or your program allocates way too much memory.

It is also worth to check if your coded uses memory efficiently.
More informations on this topic you may find in my previous talk "Everything You Always Wanted to Know About Memory in Python But Were Afraid to Ask" and references included therein. 

I/O bounds may require more effort to deal with. 
Depending on the problem there may be various solutions, consider using:

  * asynchronous I/O with Python (for example see "Journey to the center of the asynchronous world"),
  * compressed data structures and lightweight compression algorithms (i.e. algorithms that are primarily intended for real-time applications, which favours compression/decompression speed over compression ratio),
  * probabilistic data structures (like Bloom filters instead of real data).

#### Notes on the special cases

When your code involves numerics consider using numpy and scipy. 
Those libraries provide highly optimised routines (usually based on external scientific libraries).

Some problems may just need more computing power, so it may be a good idea to:
  
  * write code that utilizes multi core architecture (mutliprocessing),
  * or scale your code to multiple machines (task queues, spark, grid like environment),
  * or using hardware accelerators (pyOpenCL, pyCuda, pyMIC, etc.)

You may also consider pushing performance-critical code into C.

Remember to check your code with PyPy, you may be pleasantly surprised.

## Summary

Hopefully, this talk will help you start with Python optimisation. 

For more, checkout slides and source code examples that may be found on my website przymus.org, under "What's Eating Python performance".

## References

  1. PythonSpeed, https://wiki.python.org 
  1. PythonSpeed / Performance Tips, https://wiki.python.org
  1. Time complexity, https://wiki.python.org 
  1. PythonSpeed / Profiling Python Programs,https://wiki.python.org  
  1. Performance, http://pypy.org
  1. Everything You Always Wanted to Know About Memory in Python But Were Afraid to Ask, http://przymus.org
  1. Journey to the center of the asynchronous world, https://github.com/PyConPL/Book 
