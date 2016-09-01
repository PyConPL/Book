
Title of Presentation
=====================

[Splash](http://splash.readthedocs.io/en/stable/) is an open source scriptable headless browser with 
HTTP API written in Python 3 with Twisted & PyQt. I’d like to present the project and discuss 
couple of social and technical phenomena that I noticed while taking part in development of 
application. I’d like to discuss how application is structured, what libraries we used and
how they served us, and finally discuss how open source works for us and how I perceive it.

My presentation will have two parts, one technical and other "social/psychological". In the first 
one I'll outline application architecture. In the second one I'll try to discuss some general
issues around open source that I noticed.

What is Splash and how it works?
================================

Splash is a headless browser based on WebKit engine. Its main job is rendering HTML and JavaScript.
You can interact with Splash by sending HTTP requests with some parameters. For example you can make
request to /render.png endpoint with `url` parameter and it will send request to given url, load
it into browser window an return screenshot in .png format for you. You can also send request to
render.html endpoint and it will return html. 

Splash is scriptable, which means you can write Lua scripts that tell Splash what to do. For example
you can write script that will tell browser to click some link, wait a minute, hover cursor over
some page area and finally return screenshot of webpage after performing those actions. 

Why did we decide to create Splash? Main reason is that we needed some rendering for Scrapy. Scrapinghub
was founded by founders of Scrapy - framework for creating web crawlers. 
Today main challenge for all crawlers is JavaScript. If you want
to know how important JavaScript is for modern web try disabling JavaScript in browser and try
browsing your favorite webpages. I can guarantee you that in many cases you won't see anything. If
you do manage to browse some content you'll see terribly broken layouts, html elements completely
out of order, divs and headeings flying all over the place, missing data. In general you'll see
chaos and mayhem. Long time ago people believed in a thing called "graceful degradation", meaning that 
if user didnt have JavaScript page should still work but in a limited way. These days no one really
does graceful degradation. If you dont have modern browser with JavaScript enabled you're not able
to benefit from all the good content created by web authors. 

Now you can of course bypass these limitations, usually web pages are doing plain HTTP requests
in the background using AJAX, and AJAX is just normal HTTP request that you can imitate easily from spider.
But most people dont know this or are lazy and dont want to spend hours of their time reverse engineering web
pages by looking into developer tools, so they decide they prefer to render page. There are also some
use cases when you really need to render JavaScript (e.g. you need screenshot of page or you need
to deal with some bot protections that require you to solve JS challenge).

Why we decided to create Splash and not go with other solution? In other words why not Selenium or 
phantom JS? Main reason is that we really needed to have headless browser with HTTP API. We didnt
want to add JavaScript rendering into Scrapy but thought that having separate service doing rendering
will be better. So it was crucial to have HTTP API. None of existing JS rendering services provided
this out of the box. Now you can probably add HTTP API to existing rendering frameworks, but once you 
start doing this you realize it's hard work and it's not that easy to tie it existing software. On
the other hand getting library for rendering web pages is not difficult in Python - look no further
just use PyQt. In fact in our case rendering is done by Qt Web Kit. 

Under the hood Splash architecture is simple. HTTP API part is written in Python Twisted. It makes
heavy use of Twisted Deferred and Twisted.Resources. Main benefits it gives us is that we application
is asynchronous which is absolutely crucial for this type of task. After request is received by 
application it is forwarded to BrowserTab object. Every browser tab
object gets a web page. Web page inherits from Qt QWebView. Web page does all the rendering, it 
executes page JavaScript, renders the DOM and returns result. 

How open source works in case of Splash?
========================================

There is popular misconception that treats open source projects as some sort of charity work. In 
this perception people doing open source are mostly volunteers who just try to "help others" 
by making useful software. They dont gain anything from their work, they just contribute to projects
because of their good will. Doing open source from this point of view is similar to helping older 
people cross the street or helping starving kids in Africa. 

This perception of open source is not entirely untrue, for example Bram Molenaar author of great tool
we use and love (Vim) does encourage people to donate to kinds in Africa, but it might be sometimes 
misleading. I'd like to try to challenge this myth and try to talk about various forms of business
you can make around your open source. I'd argue that having some form of business organization around
your open source projects is good both for you and for your projects. By having some business model
you can stop relying on completely unreliable and erratic contributions of strangers. You are able 
to finance somehow development time and efforts of core team. 

Splash is nice example of how you can implement these ideas in practice so in my presentation I'd 
like to demonstrate how our particular business model works, what do we gain from open source and
why, in our specific case, its not really charity but more economic and rational calculation.

