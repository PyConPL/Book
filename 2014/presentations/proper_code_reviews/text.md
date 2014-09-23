#Proper code reviews - Tomasz Maćkowiak

Code quality is the ultimate goal that every programmer (and his manager) strives for.
High code quality means fewer bugs, better performance and easier maintenance.
One of the most popular ways of ensuring quality of the code (apart from peer programming)
is to implement code reviews.

Not all code reviews are equal. Some developers are better at it, while others
add no value in their comments.This article presents my
approach to code reviews that has worked well for me and my team for about a year already.

## What are code reviews?

This article is about informal, individual code reviews. We develop our code
using Git version control system. The model we use is feature-branching, which means
that there is a new Git branch created off the master branch for each feature
or bug fix. Developers work on this branch and, when done, they
release a pull request. The pull request is then reviewed by at least 2 other
developers. Either the original developer needs to address the review comments and
release fixes for issues found during code review, or the pull request can be
merged straight away.

## Why do you do code reviews?

The most obvious answer to the above question is to keep high code quality.
Two additional developers scrutinising all the code which gets into the repository are
supposed to find mistakes, ineffective bits, convention violations and other
issues that might be improved. The value of code review seems to be indisputable,
but there are different ways of approaching reviews, some more beneficial than others.

Code quality is not the only benefit of code reviews. What are the others?

### Standards

Thanks to code reviews, the team is bound to develop coding standards and adhere
to them. Be it standards like PEP8, the usage of `%` operator against `format` function,
to certain ways of using external libraries; over time the team reaches a consensus
and everybody needs to act on its terms, unless they want to have their
pull request rejected. At first there might be a few ways of doing something, but
in the process of performing regular code reviews alternatives are being flagged and one winning
solution emerges. In our team history we organised meetings following some particularly
heated code review discussions, where we had to pick one standard over the other.

### Knowledge sharing

If code reviews are performed properly (the whole team is obliged to carry them out
and is notified about all pull requests and comments), then code reviews also serve
the purpose of sharing knowledge among team members. That is how the above
mentioned standards are being announced - team members learn from  pull review's comments
that a certain solution is preferable to the other.
Also, the team learns other good practices. We are supposed to learn from our own
mistakes, but learning from the mistakes of our colleagues is even better.
The team starts to single out undesirable patterns if they are being flagged in code reviews.
Provided that code review is done properly and the comments hold value (for example:
*for performance use `set` here*), it can constitute an invaluable lesson.
Another important function of code reviews is that they enable team members to track what is going on in the project. The team
sees the code being committed to the repository and they know what functionalities
are being introduced and how they are implemented.

### Ownership

The code is not supposed to be the private property of the developer who first wrote it.
When practising code reviews, the reviewers share the responsibility
for the code. If the code works poorly or does not work at all, the reviewers are
guilty of letting its defects slip through their fingers. Another benefit is that there is always an opportunity for somebody
else to fix the mistake in the code, because they are at least vaguely familiar with the code,
since they browsed through it during code review.

### Personal development

There is no faster way of improving your skill than to have somebody systematically
point out your mistakes and (maybe) show you how to fix them. You improve
your code every time you receive a comment in pull request. You gain knowledge and
learn good practices from other people's pull requests. You post your own comments
to other people's code and you are able to see if your opinions are valid.


## How to do code reviews?
Code reviews only hold value if they are done properly.

### Tools

One of the key factors in effective code reviews are tools. If submitting your code for pull request or reviewing the code takes too much effort, people will simply refuse to do it. The process needs to be automatised
as much as possible. Email notifications about pull requests and comments help
a lot, because even if you do not actively follow open pull requests, you are still
notified about the progress.
My recommendation is having a private Github. It supports email notifications,
integrates into your source code repository, has a great interface and makes it
really effortless to create a pull request as well as to review one.

### The actual review

Depending on the size of the pull request, code review can take anywhere from
5 minutes to half a day in extreme cases. Since concentrating on the code under
review requires a clear head, you need to allocate an appropriate amount of time
for the review. It is preferable to do review in-between tasks,at the beginning
of the day (as a warm-up), or at the end of the day when you are too tired to keep on developing your own task anymore.

The code you are reviewing is most probably connected with a story or a bug
in your issue tracking system. It is a good idea to first read about the issue so
that you know what is to be implemented with the code.

In my opinion, you should never run the code you are reviewing. Running the code
might give you a false impression that the code is acceptable and that it works as intended, while
under the hood it is a mess.

## Good review and bad review

What should you point out during code review to make your colleagues regard it
as valuable input and not nit-picking?

Code review is done by qualified humans for a reason. You should not treat code
review as another round of PEP8 checks - these should be done by the code's author
before he creates a pull request. What if the author did not run his changes through
PEP8 check? You still should  not bother since doing something
that a machine can do in under 1 second is never worth your time and effort. It is helpful to have PEP8 as part of your
Continuous Integration suite as it prevents any potential PEP8 violation from slipping through
to the master branch. Nobody appreciates comments about different possibilities
of breaking newline in their code.

There are a few other types of comments that are annoying to developers, whereas,
contrary to popular belief, they do bring in value. People very much dislike
comments (for Python2) about changing strings to unicodes, for example in labels,
especially if the string does not contain any non-ascii characters. Their argument
is that *it doesn't matter anyway*, but in reality this error shows that the programmer
does not understand the difference between byte-strings and text-strings.
Even though such comments might seem annoying and repetitive, they do
improve the code and foster the understanding of the language’s fundamental structures.

A different kind of apparent nuisance is when the reviewer points out the inconsistencies
of your code with the project's standards. For example, the usage of `format` might
be preferred over the `%` operator. The usage of the latter is not an error per se
but it goes against project policy. This kind of comment might be annoying,
but in the long run abiding to the policy improves the coherence of the code and
makes it easy to get into it by junior developers.

Another annoyance might be calling for docstring of functions or classes.
Docstrings are almost always a good idea, unless you have a simple getter function
with a sensible name; then it might not be needed. Asking for docstrings to
all functions in review might be alleviated by using automatic tools like pylint,
which can do that for you.

During code review one might encounter pieces of code that are complex and non-trivial
to understand at first glance, or require significant effort to analyze and understand.
It is worth to ask the original developer to insert a comment describing the
particularly hard bit so that programmers down the line will not have to spend half
an hour analyzing the code just to learn what it was supposed to do.

When developers write comments and docstring, they usually need to use English
which is a foreign language to most. The level of familiarity with the language
is often visible in the comments. Incorrect grammar, misspellings etc. can make
the comment hard to understand. It is a good idea to point out such issues during
code review so that all your documentation is grammatically correct and understandable.

The most valuable comments during code review, though, are about the more high-level issues.
Comments about architecture should be greatly appreciated. Pointing out that
some code can be extracted to a helper or that some piece of code does not belong
here but somewhere else, can greatly improve the maintainability of the code.

Quite often, experienced developers can point out that code under review does not
need to be written at all, because there is already a built-in or a helper
somewhere in the project that performs the same function. Such comments are usually
only to be expected from highly experienced developers, but they carry a great
learning potential for the more junior ones.

A similar case can be made with applying correct data structures and using
efficient algorithms. An experienced developer can spot
fragments of the reviewed code where the usage of a dictionary data structure can greatly improve its performance.
Such a remark requires a higher order understanding of the purpose of the code
- it goes beyond the meaning of a single line of the code, but pertains to the the overall
result that the developer is trying to achieve.

It is fairly easy to review a code change where somebody has just added a few lines to a function.
It is, however, much harder to analyze code that introduces conditional logic. This is usually
the point at which the reviewer needs to stop and look deeply into what is happening. Analyzing
the conditions and their effects can provide one of the most valuable feedbacks
possible. The reviewer needs to ask himself the following questions: *what does this condition really mean?*,
*when is this condition not met?*, *what happens when the condition is not met?*,
*is this condition really needed?*. Some programmers try to solve problems
by introducing a number of `if` statements with complicated conditions. In many
instances such pieces of code can be refactored to a much simpler form, decreasing
the code complexity significantly and making it much more readable.

An experienced reviewer is often able to provide (just by looking at the code)
instances of corner cases in which the code would fail or predict a situation that the original
developer did not anticipate. Spotting such cases directly prevents live
system bugs and is therefore of immense value. It often requires applying a very deep and meticulous
review process, but the time spent on it is not wasted. You should not, therefore, cut down
the amount of time spent on a pull request, but rather review it until you understand it fully.

## Summary

Code review is one of the most valuable tools for assuring software quality.
When done by experienced developers who devote enough time to it, it provides an opportunity to
spot potential bugs, performance bottlenecks, or hard-to-maintain bits.
Apart from the reviewers doing their job well, the developers under review also
need to learn to embrace the critical comments and understand that code review is not a nuisance, but something that is done for their benefit.
