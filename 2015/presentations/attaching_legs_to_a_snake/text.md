# Attaching legs to a snake - or - Python3 extensions - Tomasz Maćkowiak

## Introduction

Python is a powerful language by itself. The robust standard library and the myriad of additional packages make it a Swiss Army knife of programming languages. But sometimes it is not enough. When you need to integrate with a low-level C API or execute heavy computations without the interpreter overhead, writing a Python extension module might be a good idea.

This artice will show you how to write, build and run an extension; what C API you can use in it and what to remember about; how to link to shared libraries and what does Boost.Python simplify.

## Why?

Python is a powerful language by itself. As far as the motto goes it comes *with betteries included*. There are plenty of built-in modules and there's a myriad of additional packages available at your fingertips. Whatever you want to do, there's high chance somebody already wrote a package for it.

But what if nobody did? But you need to integrate with some low-level C library or you need your calculations to run faster and you can't implement them in pure Python because of the interpreter overhead?

Then you can write a Python extension module in C or C++ that will integrate with the rest of your Python project on one end and with low-level primitives on the other end.

## Other solutions - or - you don't always need an extension module

## Basic anatomy of an extension

## Configuration and building

## Python C API

## Linking to a library

## Boost.Python

## References

## Threading

## Summary

