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
Usually the first part of your system showing some symptoms will be your database, this will usually be your first bottleneck and the first thing you'll have to optimize.

#### Increased response times
This is the main symptom, and it could be the product of either slow reads or slow writes, which leads to slow reads due to resource locking.

- **Slow writes:** usually product of over-indexing a table, all indexes are updated on write time on `INSERT`, `UPDATE` and `DELETE`. Too many indexes on a table will produce slow writes, no indexes at all might end up on slow reads, you need to know your data model and the questions it needs to answer and index based on workload. Premature optimization is bad.

- **Slow reads:** could be the product of a sub-optimal data model for the type of queries it needs to answer, solutions will depend on the traffic on the tables and the relations between them.
    - **Add Indices:** a good hint about which fields to index is to check the ones that appear the most on the `WHERE` clauses of the executed SQL queries. It's usually a good idea to index foreign keys.
    - **Denormalize:** usually it's a bad idea to add `ManyToMany` relations between model we know will grow indefinetely and quick, consider denormlizing them into `JSONField` or `ArrayField` if using Postgres or just duplicate the data, this will drastically improve the performance on those queries.
    - **Database caching:**

### Caching


## Conclusion