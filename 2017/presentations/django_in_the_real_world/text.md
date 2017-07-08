# Django in the Real World - Israel Fermín Montilla

## Introduction
There are hundreds of django-based projects running out there, in most of the cases, the default setup is enough. Some others need to scale so
they can serve thousands of requests per minute. Even though there's no recipe for optimization, there are some strategies ou can implement to
take your project to that level, some of them are very simple, some others are very complex.

Optimizing a system, isn't always related to the technology or the tools you're using. Of course, there are efficient and inefficient ways of
using certaing language or framework, but it's usually more about having some Software Engineering concepts clear and knowing how to apply 
them to your current technology of choice after measuring your performance metrics.

## Basic Concepts
* **Performance:** is the amount of work accomplished by a computer system. There are several metrics to measure how a system performs, depending on the case, the most common metrics are:
    * **Response time:** total amount of time it takes to a system to respond to a request for service;
    * **Throughput:** is the maximum rate at which *something* can be processed. For web systems it's usually measured in *requests per minute*;
    * **High availability:** it's a charasteristic of systems which aims to ensure a certain level of operational performance, usually *uptime*, for a higher period of time;
    * Low utilization of available resources.

* **Scalability:** the capability of a system to process or handle a **growing** workload or its potential to be **enlarged** to accomodate that growth is known as Scalability. We say a system is **scalable** if its performance improves after adding more hardware proportionally to the added capacity;

* **Bottleneck:** a *bottleneck* occurs when the capacity of an application is severly limited by a single component. The *bottleneck* has the lowest *throughput* of all the parts of the transaction;

* **Pareto principle:** the *pareto principle* states that, for many events, roughtly 80% of the efects come from 20% of the causes, so, by fixing that 20%, we could achieve an 80% improvement.

## Basic django deployment
The usual django stack runs django with either *uwsgi* or *gunicorn* behind a web server that could be either apache or nginx and uses *postgres* for database persistence, the architecture would be something like this:

### TODO: architecture diagram

This would be how you'd deploy your personal project to your VPS for the first time.

## Common bottlenecks
However, you can't keep that architecture forever, as traffic grows, some parts of the system will suffer and you'll have to use some strategies to relief that pain.

### Database level
Usually the first part of your system showing some symptoms will be your database, this will usually be your first bottleneck

### Caching


## Conclusion