---
layout: heartbeat
category: blog
tags: [android, iOS, open-source]
date: 2014-06-24 00:00:00
title: Optimizing API against latency
author:
 - id: wojtek_erbetowski
description: |
    We share our experiences of optimizing mobile-dedicated, practical-REST API avoiding latency problems with merging responses, HATEOAS and HTTP cache

---

Designing an API is an incredibly important moment for a project’s future. 
Every change made in the future will be accompanied by having to support multiple versions of an API, modifying docs, server-side code and the client. 
Because of this laundry list of changes to keep track of, we try to solve as many design problems as possible up front.  
There are several different areas, that make a huge impact. The one we target in this post is latency.

> Latency is a time interval between the stimulation and response (...).
> <cite>Wikipedia, Latency (engineering)</cite>

What is latency when it comes to mobile devices? 
Mobile networks are still far from what we would call high performance. 
There is huge overhead required when you make even a single request from your mobile app. 
A quick list of the steps needed:

- RRC negotiation
- DNS lookup
- TCP handshake
- TLS handshake
- HTTP request

Beyond just this one complicated path, we need to keep in mind some potential problems:

- weak signal
- lost signal 
- client is moving and changing base stations
- routing gets mixed up - [source](http://calendar.perfplanet.com/2012/latency-in-mobile-networks-the-missing-link/)
- different pings originating from the same location(home/office) - [source](http://blog.cloudflare.com/why-mobile-performance-is-difficult)

You end up with a latency of 100ms-300ms for 3G networks and up to 1000ms for 2G. 
Since 2G is becoming obsolete and 4G is just around the corner for our users (check this [thread](http://serverfault.com/a/573815)), 
let's take a look at a forecast from Cisco Systems, Inc. ([source](http://www.cisco.com/c/en/us/solutions/collateral/service-provider/visual-networking-index-vni/white_paper_c11-520862.html)).

![CISCO mobile connection speed forecast](cisco.png)

What this shows is that 4G shouldn't be treated as the representative network connection of our users. 
Of course we should be able to target our application well and if it's an app for geeks, 
let's say a [StackOverflow](http://stackoverflow.com/) client, the subsequent network connection speed will be drastically higher 
than when compared to a general purpose app like a news reader.  

We can deal with latency by trying to optimize DNS lookup counts, shorten the request route, and many many more. 
We could even go so far as to spend [25 million dollars](http://www.extremetech.com/extreme/122989-1-5-billion-the-cost-of-cutting-london-toyko-latency-by-60ms) to improve it by another 1ms. 
However, this article is addressing a rather specific part connected to API design. 
So, how can we influence the latency by API design?

### Merging responses

First, let's make a use of an example. Let's say we have a view that says user name, age and country. 
Name and age are a part of `/users/{id}` resource:

```json
{
  "name": "John Doe",
  "age": 25,
  "links": [
    {
      "rel": "self",
      "href": "/users/123"
    },
    {
      "rel": "account",
      "href": "/accounts/987"
    },
    {
      "rel": "address",
      "href": "/users/123/address"
    }
  ]
}
```

To display a country, we need to make another call, for `/users/{id}/address`. This means following the entire route to reach the server again:

```json
{
  "street": "Sesame",
  "no": 25,
  "zipCode": "12-321",
  "state": "NY",
  "country": "US"
}
```

But since there's no real reason to make both of those calls, let's try to save one connection and prepare a special endpoint, dedicated for that screen:

```json
{
  "name": "John Doe",
  "age": 25,
  "counry": "US"
}
```

Now instead of making two separate calls we may just call a single endpoint and get all of the required information. 
But remember that there is a tradeoff. To get a more robust API we're stepping away from a REST design pattern 
and binding together two related entities - user and address.

### Expansion

We don't always know the way in which our API will be used. 
In the last example we implicitly assumed that we knew what information was being displayed. 
But what about cases where we design a service for future consumers which may present data in any way they decide? 
Yet we still want to give the option to optimize answers.

In that case an expansion pattern becomes very handy. 
Going to our previous example, what would this look like? 
We need to prepare a request that specifies which fields to display (and embed from related entities). 
`GET /users/123` now becomes `GET /users/123?fields=[name,age,address[country]]`.

```json
{
  "name": "John Doe",
  "age": 25,
  "address": {
    "counry": "US"
  }
}
```

This is a pretty neat mechanism for merging responses, although it has it's own limitations as well. 
If API consumers are using relations, we won't be able to change the resource hierarchy without breaking clients.

### Keep-alive

The closing trick is to make sure your service supports the HTTP keep-alive option. 
By default, all mobile HTTP clients will try to sustain the HTTP connection between different calls so it makes perfect sense to utilize this. 
If the server will agree to keep the connection, the next requests will omit several handshakes and directly be sent to server within an opn connection.

### Closing word

In Polidea we are developing mobile apps and supporting them with backend services.
The last couple of years has taught us that you may not achieve a proper user experience without slick HTTP communication.
This article was inspired by our experiences from real-world projects.
As always, we welcome any feedback and would be happy to discuss this topic as well as our work in further details.

