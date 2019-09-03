## Abstract

Introducing agility into an organization is not an easy task, not matter if you do it in a stale organization or a completely fresh one.

What’s to blame? Our inherent nature, for one, as we are creatures of hierarchy. Self-organization is not as natural to us as we would like to think. But equally important are the misconceptions about agile in general and the lack of appreciation for software patterns.

Let’s look at those misconceptions, the culture of agility, and what *processes and tools* to apply to the code once we’ve transformed the *individuals and interactions*.

## Let’s do Agile!

What does introducing agile to a company usually look like? A manager learns of a methodology which speeds up development and requires less up-front planning, called “Agile”. They assume it saves money, produces more features and Makes Development Great Again. So obviously they want to jump on board.

Let’s say they go online and try to look for resources on the subject. Chances are they come out with a very strong conviction that “doing Agile” effectively means Scrum, and Scrum, in turn, means sprints. Before you know it, a JIRA license is bought, someone is titled Product Owner and they begin stuffing all the current tickets in a backlog, creating a *five year plan* cut up in 2-week packets.

Given that Scrum is a process (actually a framework, but for the sake of argument) and JIRA is a tool, stack that against *The Agile Manifesto’s* first and foremost point: “Individuals and interactions over processes and tools” and you know something’s backwards. An agile revolution is a change of who you are, not of what you do. “Agile” is an *adjective*. “Doing agile” makes about as much sense semantically as “doing purple”.

## A lesson from General Motors

Between the late 1940s and 1970s Toyota came up with a process now called the TPS - Toyota Production System. It allowed them to produce better quality cars at a much lower cost than anyone thought possible, so obviously American manufacturers tried to imitate it.

In fact, Toyota encouraged it and gave tours of it’s factories. They knew you can copy the tools and the processes, but it’s the culture that makes them work. And you can’t copy that culture just by looking at people screwing cars together. Plus, Toyota’s agile mentality also meant they would’ve improved on the processes before their competitors landed back in the US.

Part of the TPS is a tool - the Andon Cord. Whenever an assembly line worked notices a quality issue, they pull on that cord and the line stops. At that point engineers gather around and figure out how to solve the issue, before you have a lot of defective cars no-one wants to buy. Or, in other words, before you become General Motors of that time.

The cord worked in Japan and it was one of the things GM copied. After a while, they were surprised to find that the TPS is crap. It cost more, made less cars and the quality was just as bad as ever. Yeah, well, they kind of forgot the cord doesn’t work if people are afraid to pull it.

You see, GM had an authoritative, hierarchical structure. The engineers were there to design the cars and the peasants at the assembly line were there to put them together. If something didn’t fit, it was a peasant problem and the engineers were not to be bothered with such mundane matters.

The whole company was focused on utilization - making the most of their work force and getting as many cars of the line as possible. This doesn’t resonate with the idea of stopping the assembly line until you figure out a way to not have Tesla Model 3 panel gaps on your cars. You can’t be agile if you’re afraid to slow down.

## The legacy of low agility

Consider a software system built by a “1970s GM of software”. High pressure, impossible deadlines, badly understood business requirements and utilization as a measurement of productivity. That in mind, let me introduce you to the *Conway’s law:*


> organizations which design systems ... are constrained to produce designs which are copies of the communication structures of these organizations.

That software will have an accidental architecture, molded by all the shortsighted time- and cost-saving decisions. It won’t have an automated deployment pipeline or test coverage, because ain’t nobody got time for that. It’s gonna be a mess.

Let’s now put effort (and sweat and tears) into reshaping the organization so it has a flat structure full of trust. Imagine its culture turned into a 1970s Toyota with a management process as lean and agile as a Parkour runner. Bad news, though - it still won’t deliver a single sprint.

Why? Because you now have a very agile organization working with legacy code, written in a non-agile era. Everyone’s eager to pull on the *adon cord*, but there’s none and they’re actually stuck at a Ford Model T-style production line.

Luckily, having the right culture (a better guide to getting there is beyond the scope of this text, sorry), you can start using the right tools and processes to bring your code into the new era. But first, let’s try to understand how that big ball of mud we call “legacy code” came to be in the first place.

## Short term benefits, long term headaches

Let me use an example of a decision made early on, which can have dire consequences. Using the ORM as your domain entities and an SQL database as your domain model.

At first, this sounds reasonable enough that people tend to accept it with little thought. It’s actually what tutorials tell you to do. And while it’s good enough for simple projects (like a blog), these are some very serious assumptions to make up front, which are difficult to back away from.

After a while you may consider getting your data from places other than SQL. NoSQL document storage, a graph database, an object database or even some entirely external service. Moreover, a single domain entity could be sourced from a combination of these, but doing that without layers of indirection (when ORM is your business logic) requires working around your own architecture. Get a large enough project and the problem will only grow with time.

This is where accidental complexity comes from - starting with a locked down decision and trying to work around it. That is the exact opposite of agility.

## Digging yourself out

Ok, but how do we make an agile revolution happen in legacy code built by a non-agile company?

*Gradually.*

Of course you could just create a new repo and start rewriting the whole thing, but that’s called the *second system syndrome*. Possible outcomes?


1. it never reaches production and you just stay with the old system
2. your organization goes bankrupt because it could not keep up with the competition
3. you start to rush it at some point and end up with even more mess.

So that won’t work. We’re stuck with re-shaping the existing system. For that, let's turn to David Wheeler’s *fundamental theorem of software engineering*:


> All problems in computer science can be solved by another level of indirection

And follow the advice the advice from Kent Beck, so we don’t try to do everything at once:


> for each desired change, make the change easy (warning: this may be hard), then make the easy change

The procedure to follow is not so different from the standard TDD *Red-Green-Refactor* cycle.

## Test coverage

Face the facts - it doesn’t have tests. In fact, looking at legacy projects I find an interesting correlation - the less important a piece of code, the more test coverage. Some irrelevant CSV exporter? 100% branch coverage. The master function doing everything from user log in to firing nuclear missiles? A single test. For a happy path. And it’s probably commented because it didn’t work.

It will be ugly, but there’s no other way - make sure you cover as much business logic as possible. Take that opportunity to learn the system. It might even be impossible to tell what states it may have, so operate under the assumption it runs on magic. Preparing the *interactive specification* (aka the test suite) will let you understand all the quirks and notice the areas for improvement.

However, do not attempt to fix or refactor anything at this point. Seriously, don’t. Only once you’re satisfied with the test suite can you try to renovate the whole thing.

## Code for deletion

Feature flags we usually associate with A/B testing and relatively small changes like the placement or shape of a button. In reality, it’s a great tool to increase the agility of your code.

Using feature flags you can make serious changes gradually, while pushing them continuously to production. It limits the risks involved with deploying changes and helps you avoid merge conflicts and work better as a team - all great things if you want to score agility points.

Most importantly though, it also shapes the way you (re)build the code. It will force you to increase cohesion and reduce coupling. Eventually, you will just replace code instead of modifying it, which is the ultimate goal when it comes to code agility.

If you now think “what about changing the data base schema, I can’t run two schemas at the same time!” You’re right, you (usually) can’t. But your business logic shouldn’t really care about your database schema, only about entities. That’s what the *“Short term benefits, long term headaches”* section was about. Choosing to support feature flags will, again, motivate you to reduce that coupling.

A cool side-effect of being able to run two versions side by side is you can make sure they do the same thing before making a switch. Once you’re confident, you just scrap the old one - leaving only the new and shiny code. Stress reduction is always a nice bonus.

## Plumbing

Another great way of learning new things about your system and forcing yourself to think of how it should be structured is plumbing  - working on your pipelines.

Tiny, throw-away systems obviously don’t need the whole “continuous deployment with automated horizontal scaling architecture as code” shebang, but if you got this far in this text, yours probably does (or you’re just curious, which is also great).

Among other things, it helps you understand the value of configuration. Most programmers don’t really consider it *code,* yet a config file is just as much a piece of code as anything else. You realize that as soon as you have to push everything through a pipeline in a tractable and secure way.

## Set the stage

Staging. If you don’t have one - get one. If you do, ask yourself a very serious question: is it really? Many staging environments I’ve seen are in fact glorified testing servers. Either they don’t resemble the production infrastructure at all or they’re full of old code which never ended up on production. Or both.

Since you’re already looking at your staging, take a look at your repository as well. Got some unfinished or un-deployed code on staging? Then your workflow probably looks something like this:

```
    * Merge feature into production
    |\
    |  \
    | * | Merge feature into staging
    | |\|
    | | * feature
    | | |
    * |/ ...
    |/|
```

Staging is meant to be a stop on your path to production, just as it is in QA. Yet in the repo stuff is merged into production without going *through* staging, which means staging will drift away - there’s really nothing blocking you from creating a huge branch with a multitude of changes, merging it into staging and leaving it there indefinitely. Or merging into production without going through staging.

A better alternative? There are numerous options, but  you generally don't want to merge your feature branches into more than one place. For instance:

```
    * Merge feature into production
    |\
    | * Merge feature into staging
    | |\
    | | * feature
    | * | ...
    | |/
    | |
```

Again, the purpose of this is to make it *inconvenient to do the wrong thing*.

Made a huge, conflict-inducing branch and merged it into staging? You get punished by a freeze on your entire pipeline. Again, this workflow promotes incremental changes and small PRs. It amplifies the need for feature flags. It forces you to change your thinking from short term convenience to *sustainability*.

Ideally, you get to a point where your feature branches live for a day or two before they’re merged, and they build on each other, making code review a breeze. Another huge benefit.

## Suggestions, not commandments

While I believe following these rules is beneficial, context matters! As Kevlin Henney likes to put it, looking left when crossing a one-way street is a great rule in continental Europe but a quick way to get yourself killed in the UK. Same with this.

The point of Clean Architecture (and the likes) is to push important decisions as far away as possible. Sometimes, though, the most important decision is whether or not you need these rules at all, because they do come at a cost. Sure, they help you avoid accidental complexity, but intentional complexity is just as bad when it serves no purpose.

Software design patterns are there for a reason, but just like Scrum, Kanban and the TPS, they don’t exist in vacuum. They’re there to help you make sense of a large system, but they can just as easily *create* one. If you don’t know what I mean, just google “fizzbuzz enterprise edition”.

## Pain is good, pain means you’re alive

You’re probably noticing that most of these techniques are there to force you to do something painful. This is intentional. If you look at the history of programming, it’s basically defined by taking away freedoms. Just like that time we got rid of `goto`.

All of these things make writing individual lines of code *harder*, so writing systems and collaborating can be *easier*. In the words of Mark Seemann:


> Some developers seem to think that typing is a major bottleneck while programming. It's not.

The bottleneck is understanding what to type and what’s been typed. That’s exactly why you should be wary of everything that saves you a few minutes, because more often than not, it’s also creating a time bomb. On the other hand, there’s a good change that processes and tools which require a lot of work/learning at first, will benefit you in the long run.

## Sources
1. Martin, Robert C. (2017). Clean Architecture: A Craftsman's Guide to Software Structure and Design
2. Jez Humble, Barry O'Reilly, Joanne Molesky (2014). Lean Enterprise: How High Performance Organizations Innovate at Scale
3. Kevlin Henney, https://www.youtube.com/playlist?list=PL6wxfKvkNqRugfIiKKgRXa_0wKIQW_ZEH
4. Greg Young - The art of destroying software, https://vimeo.com/108441214

